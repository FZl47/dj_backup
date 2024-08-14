import abc
from dj_backup.core import utils
from dj_backup import settings


class BaseBackup(abc.ABC):

    def __init__(self):
        # check temp dir is exists or create it
        temp = settings.get_backup_temp_dir()
        utils.get_or_create_dir(temp)
