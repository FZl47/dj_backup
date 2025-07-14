import abc
import shelve
import time
import sys
from typing import Callable, Optional, List, Dict, Any

from django.utils import timezone

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler as _BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

from dj_backup import settings
from dj_backup.core.utils import random_str, log_event
from dj_backup import models

from .common import Task


class StorageBase:
    _db_name = 'dj_backup.db'
    _list_key = 'new_tasks'
    _list_delete_key = 'delete_tasks'

    @classmethod
    def _get_connection(cls) -> shelve.DbfilenameShelf:
        """
            Returns a connection to the backup database.
        """
        return shelve.open(f'{settings.get_backup_sys_dir()}/{cls._db_name}')


class StorageBackground(StorageBase):
    def get_tasks(self) -> List[Any]:
        """
            Get and return new tasks created.
        """
        c = self._get_connection()
        d = c.get(self._list_key, [])
        c.close()
        return d

    def get_delete_tasks(self) -> List[Any]:
        """
            Get and return tasks that need to be deleted.
        """
        c = self._get_connection()
        d = c.get(self._list_delete_key, [])
        c.close()
        return d

    @classmethod
    def flush(cls) -> None:
        """
            Clear the list of new tasks in the storage.
        """
        c = cls._get_connection()
        c[cls._list_key] = []
        c.close()
        log_event('StorageTask: Tasks list flushed !', 'DEBUG')

    @classmethod
    def flush_delete_tasks(cls) -> None:
        """
            Clear the list of tasks to be deleted in the storage.
        """
        c = cls._get_connection()
        c[cls._list_delete_key] = []
        c.close()
        log_event('StorageTask: Delete tasks list flushed !', 'DEBUG')


class StorageTask(StorageBase):

    def remove_task(self) -> List[str]:
        """
            Remove a task by its ID.
        """
        return self.remove_task_by_id(self.task_id)

    @classmethod
    def remove_task_by_id(cls, task_id: str) -> List[str]:
        """
            Mark a task as deleted by adding its ID to the delete list.
        """
        c = cls._get_connection()
        d = c.get(cls._list_delete_key, [])
        d.append(task_id)
        c[cls._list_delete_key] = d
        c.close()
        log_event('StorageTask: Delete task signal created', 'DEBUG')
        return d

    def add_task(self) -> List['StorageTask']:
        """
            Add a new task to the storage.
        """
        c = self._get_connection()
        d = c.get(self._list_key, [])
        d.append(self)
        c[self._list_key] = d
        c.close()
        log_event('StorageTask: New task signal added to runner', 'DEBUG')
        return d


class ListenToTasksSignals(abc.ABC, StorageBackground):
    def listen(self) -> None:
        """
            Start listening for task signals (new tasks and tasks to delete).
        """

        def handler() -> None:
            while True:
                # Delete tasks and remove from job list
                delete_tasks = self.get_delete_tasks()
                for task_id in delete_tasks:
                    try:
                        self.remove_job(task_id)
                        msg = "Job '{}' deleted at {}".format(task_id, time.strftime('%H:%M:%S'))
                        log_event(msg)
                        sys.stdout.write(msg + '\n')
                    except JobLookupError:
                        log_event("Job '{}' not found to delete {}".format(task_id, time.strftime('%H:%M:%S')),
                                  'warning')
                if delete_tasks:
                    self.flush_delete_tasks()

                # Create new tasks and add to job list
                tasks = self.get_tasks()
                for task in tasks:
                    self.add_job(task)
                    msg = "Job '{}' received at {}".format(task.task_id, time.strftime('%H:%M:%S'))
                    log_event(msg)
                    sys.stdout.write(msg + '\n')
                if tasks:
                    self.flush()
                time.sleep(settings.listen_to_tasks_time_loop)

        t = Task(func=handler, f_kwargs={'daemon': True})
        t.run()


class TaskSchedule(StorageTask):

    def __init__(self, func: Callable, seconds: int, repeats: int = -1, task_id: Optional[str] = None,
                 strict: bool = True, f_args: Optional[List[Any]] = None,
                 f_kwargs: Optional[Dict[str, Any]] = None) -> None:
        """
            Initialize a new task schedule with function, interval, and repeat settings.
        """
        self.func = func
        self.seconds = seconds
        self.repeats = repeats
        self.task_id = task_id or random_str(40)
        self.f_args = f_args or []
        self.f_kwargs = f_kwargs or {}
        # Add task_id to kwargs
        self.f_kwargs['task_id'] = self.task_id

        if models.TaskSchedule.objects.filter(task_id=self.task_id).first():
            msg = f"The task object must be unique, an object with this ID '{task_id}' already exists."
            log_event(msg, 'warning')
            if strict:
                raise ValueError(msg)
            else:
                return

        self.task_obj = models.TaskSchedule.objects.create(
            task_id=self.task_id,
            func=self.get_func_content(),
            seconds=self.seconds,
            repeats=self.repeats,
            args=','.join(self.f_args),
            kwargs=self.f_kwargs,
        )

        self.add_task()

    def get_func_content(self) -> str:
        """
            Get the content (filename and function name) of the function being scheduled.
        """
        c = self.func.__code__
        return f'{c.co_filename}:{c.co_name}'

    def get_task_obj(self, task_id: str) -> Optional[models.TaskSchedule]:
        """
            Retrieve the task object by its ID.
        """
        try:
            if not self.task_obj:
                self.task_obj = models.TaskSchedule.objects.get(task_id=task_id)
            return self.task_obj
        except (models.TaskSchedule.DoesNotExist,):
            self.remove_task()
            return None
        except (models.TaskSchedule.MultipleObjectsReturned,):
            return None

    def handler(self, *args: Any, **kwargs: Any) -> None:
        """
            Execute the task and update its status in the database.
        """
        task_id = kwargs['task_id']
        task_obj = self.get_task_obj(task_id)
        del kwargs['task_id']
        if not task_obj:
            log_event('Task:handler `{}` is None object'.format(task_id), 'warning')
            return

        if not task_obj.is_available:
            log_event('Task:handler `{}` is not available anymore'.format(task_id), 'warning')
            return

        if not task_obj.is_available_for_run:
            log_event('Task:handler `{}` is not available for running [task has stopped]'.format(task_id), 'warning')
            return

        try:
            self.func(*args, **kwargs)
            msg = "Job '{}' Successfully done at {} !".format(task_id, time.strftime('%H:%M:%S'))
            log_event(msg)
            sys.stdout.write(msg + '\n')
        except Exception as e:
            msg = "Job '{}' Failed at {} ".format(task_id, time.strftime('%H:%M:%S'))
            log_event(msg, 'ERROR', exc_info=True)
        finally:
            # Update task object
            task_obj.last_run = timezone.now()
            task_obj.count_run += 1
            task_obj.save(update_fields=['last_run', 'count_run'])

            if self.repeats > 0:
                if task_obj.count_run >= self.repeats:
                    # Stop and delete task
                    task_obj.delete()


class BackgroundScheduler(_BackgroundScheduler, ListenToTasksSignals):
    executors: Dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
            Initialize the background scheduler and configure it.
        """
        self.set_config()
        super().__init__(executors=self.executors, *args, **kwargs)

    def set_config(self) -> None:
        """
            Set the configuration for the background scheduler.
        """
        self.executors = {
            'default': ThreadPoolExecutor(max_workers=settings.get_max_workers_count())
        }

    def start(self, *args: Any, **kwargs: Any) -> None:
        """
            Start the background scheduler and listen for task signals.
        """
        self.listen()
        super().start(*args, **kwargs)

    def add_job(self, task: TaskSchedule, *args: Any, **kwargs: Any) -> None:
        """
            Add a new job to the scheduler.
        """
        task_obj = task.get_task_obj(task.task_id)
        if not task_obj:
            log_event('Task:add_job `{}` is None object'.format(task.task_id), 'warning')
            return
        if not task_obj.is_available:
            log_event('Task:add_job `{}` is not available'.format(task.task_id), 'warning')
            return
        super().add_job(
            task.handler, trigger='interval', args=task.f_args,
            kwargs=task.f_kwargs, id=task.task_id,
            seconds=task.seconds, *args, **kwargs)
