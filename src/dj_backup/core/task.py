import time
import abc
import threading
import schedule
import queue


class BaseTask(abc.ABC):
    """abstract base task class"""
    QUEUE = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def run_on_thread(cls):
        def queue_main_worker():
            queue_obj = cls.get_queue()
            while 1:
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
        self.get_queue().put(task_obj)

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class Task(BaseTask):
    pass


class BaseScheduleTask(BaseTask):

    @classmethod
    def run_on_thread(cls):
        super(BaseScheduleTask, cls).run_on_thread()

        def schedule_main_worker():
            while 1:
                schedule.run_pending()
                time.sleep(1)

        schedule_thread = threading.Thread(target=schedule_main_worker)
        schedule_thread.start()


class ScheduleTask(BaseScheduleTask):
    pass


class ScheduleFileBackupTask(BaseScheduleTask):
    def __init__(self, interval, *args, unit='hour', **kwargs):
        super(ScheduleFileBackupTask, self).__init__(*args, **kwargs)
        self.interval = interval
        self.unit = unit
        j = schedule.every(interval)
        j.unit = unit
        j.do(self.add_to_queue, self)

    def __call__(self):
        
        print('Working ', self.args, self.kwargs)


BaseScheduleTask.run_on_thread()
ScheduleFileBackupTask(4, unit='seconds')
