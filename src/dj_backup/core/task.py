import time
import abc
import threading
import schedule
import queue
from typing import List, Literal
from .storage import FileBackup


class BaseTask(abc.ABC):
    """abstract base task class"""
    QUEUE = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


    @classmethod
    def _run_queue_main_worker(cls):
        queue_obj = cls.get_queue()
        while True:
            job_func = queue_obj.get()
            job_func()
            queue_obj.task_done()

    @classmethod
    def run_on_thread(cls):
        def queue_main_worker():
            queue_obj = cls.get_queue()
            while True:
                job_func = queue_obj.get()
                job_func()
                queue_obj.task_done()

        queue_thread = threading.Thread(target=queue_main_worker)
        queue_thread.start()

    @classmethod
    def get_queue(cls):
        if not cls.QUEUE:
            cls.QUEUE = queue.Queue()
        return cls.QUEUE

    def add_to_queue(self, task_obj):
        self.get_queue().put_nowait(task_obj)

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class Task(BaseTask):
    pass


class BaseScheduleTask(BaseTask):
    SCHEDULER = None

    @classmethod
    def get_scheduler(cls):
        if not cls.SCHEDULER:
            cls.SCHEDULER = schedule.Scheduler()
        return cls.SCHEDULER

    @classmethod
    def run_on_thread(cls):
        super(BaseScheduleTask, cls).run_on_thread()

        def schedule_main_worker():
            while True:
                cls.get_scheduler().run_pending()
                time.sleep(1)

        schedule_thread = threading.Thread(target=schedule_main_worker)
        schedule_thread.start()


class ScheduleTask(BaseScheduleTask):
    pass


class ScheduleFileBackupTask(BaseScheduleTask):
    def __init__(self, files: List[FileBackup], interval: int,
                 unit: Literal['seconds', 'minutes', 'hours', 'days', 'weeks'] = 'hours', *args, **kwargs):
        super(ScheduleFileBackupTask, self).__init__(*args, **kwargs)
        self.files = files
        self.interval = interval
        self.unit = unit
        j = self.get_scheduler().every(interval)
        j.unit = unit
        j.do(self.add_to_queue, self)

    def __call__(self):
        print('awd')
        for file in self.files:
            file.save()
        # TODO: add log
        # TODO: send notification(sms,email)

# BaseScheduleTask.run_on_thread() # TODO: should use command to run
# ScheduleFileBackupTask(4, unit='seconds')
