import abc
import shelve
import threading
import time
import sys

from django.utils import timezone

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler as _BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

from dj_backup import settings
from dj_backup.core.utils import random_str, log_event
from dj_backup import models


class StorageBase:
    _db_name = 'dj_backup.db'
    _list_key = 'new_tasks'
    _list_delete_key = 'delete_tasks'

    @classmethod
    def _get_connection(cls):
        return shelve.open(f'{settings.get_backup_sys_dir()}/{cls._db_name}')


class StorageBackground(StorageBase):
    def get_tasks(self):
        """
            get and return new tasks created
        """
        c = self._get_connection()
        d = c.get(self._list_key, [])
        c.close()
        return d

    def get_delete_tasks(self):
        """
            get and return tasks that need to be deleted
        """
        c = self._get_connection()
        d = c.get(self._list_delete_key, [])
        c.close()
        return d

    def flush(self):
        c = self._get_connection()
        c[self._list_key] = []
        c.close()
        log_event('StorageTask: Tasks list flushed !', 'DEBUG')

    def flush_delete_tasks(self):
        c = self._get_connection()
        c[self._list_delete_key] = []
        c.close()
        log_event('StorageTask: Delete tasks list flushed !', 'DEBUG')


class StorageTask(StorageBase):

    def remove_task(self):
        return self.remote_task_by_id(self.task_id)

    @classmethod
    def remote_task_by_id(cls, task_id):
        c = cls._get_connection()
        d = c.get(cls._list_delete_key, [])
        d.append(task_id)
        c[cls._list_delete_key] = d
        c.close()
        log_event('StorageTask: Delete task signal created', 'DEBUG')
        return d

    def add_task(self):
        c = self._get_connection()
        d = c.get(self._list_key, [])
        d.append(self)
        c[self._list_key] = d
        c.close()
        log_event('StorageTask: New task signal added to runner', 'DEBUG')
        return d


class ListenToTasksSignals(abc.ABC, StorageBackground):
    def listen(self):
        def handler():
            while True:
                # delete task and remove from job list
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

                # create new task add to job list
                tasks = self.get_tasks()
                for task in tasks:
                    self.add_job(task)
                    msg = "Job '{}' received at {}".format(task.task_id, time.strftime('%H:%M:%S'))
                    log_event(msg)
                    sys.stdout.write(msg + '\n')
                if tasks:
                    self.flush()
                time.sleep(settings.listen_to_tasks_time_loop)

        t = threading.Thread(target=handler, daemon=True)
        t.start()


class TaskSchedule(StorageTask):

    def __init__(self, func, seconds, repeats=-1, task_id=None,
                 f_args=None, f_kwargs=None):
        self.func = func
        self.seconds = seconds
        self.repeats = repeats
        self.task_id = task_id or random_str(40)
        self.f_args = f_args or []
        self.f_kwargs = f_kwargs or {}
        # add task_id to kwargs
        self.f_kwargs['task_id'] = self.task_id

        if models.TaskSchedule.objects.filter(task_id=self.task_id).first():
            msg = f"The task object must be unique, an object with this ID '{task_id}' already exists."
            log_event(msg, 'ERROR')
            raise ValueError(msg)

        self.task_obj = models.TaskSchedule.objects.create(
            task_id=self.task_id,
            func=self.get_func_content(),
            seconds=self.seconds,
            repeats=self.repeats,
            args=','.join(self.f_args),
            kwargs=self.f_kwargs,
        )

        self.add_task()

    def get_func_content(self):
        c = self.func.__code__
        return f'{c.co_filename}:{c.co_name}'

    def get_task_obj(self, task_id):
        try:
            if not self.task_obj:
                self.task_obj = models.TaskSchedule.objects.get(task_id=task_id)
            return self.task_obj
        except (models.TaskSchedule.DoesNotExist,):
            self.remove_task()
            return None
        except (models.TaskSchedule.MultipleObjectsReturned,):
            return None

    def handler(self, *args, **kwargs):
        task_id = kwargs['task_id']
        task_obj = self.get_task_obj(task_id)
        del kwargs['task_id']
        if not task_obj:
            log_event('Task:handler `{}` is None object'.format(task_id), 'warning')
            return

        if not task_obj.is_available:
            log_event('Task:handler `{}` is not available any more'.format(task_id), 'warning')
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
            # update task obj
            task_obj.last_run = timezone.now()
            task_obj.count_run += 1
            task_obj.save(update_fields=['last_run', 'count_run'])

            if self.repeats > 0:
                if task_obj.count_run >= self.repeats:
                    # stop and delete task
                    task_obj.delete()


class BackgroundScheduler(_BackgroundScheduler, ListenToTasksSignals):
    executors = None

    def __init__(self, *args, **kwargs):
        # set config
        self.set_config()
        super().__init__(executors=self.executors, *args, **kwargs)

    def set_config(self):
        self.executors = {
            'default': ThreadPoolExecutor(max_workers=settings.get_max_workers_count())
        }

    def start(self, *args, **kwargs):
        self.listen()
        super().start(*args, **kwargs)

    def add_job(self, task: TaskSchedule, *args, **kwargs):
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
