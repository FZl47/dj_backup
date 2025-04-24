import abc
import time

from dj_backup.core import utils
from dj_backup import settings


class BaseBackup(abc.ABC):
    time_start = None
    time_end = None

    def __init__(self):
        # check temp dir is exists or create it
        temp = settings.get_backup_temp_dir()
        utils.get_or_create_dir(temp)

    def get_backup(self):
        self.time_start = time.time()
        backup = self._get_backup()
        self.time_end = time.time()
        return backup

    @abc.abstractmethod
    def _get_backup(self):
        raise NotImplementedError

    @property
    def time_taken(self):
        if self.time_end and self.time_start:
            return self.time_end - self.time_start
        return 0
