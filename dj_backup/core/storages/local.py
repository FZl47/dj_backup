from dj_backup.core import utils

from .base import BaseStorageConnector


class LocalStorageConnector(BaseStorageConnector):
    CONFIG = {
        'OUT': None,
    }
    STORAGE_NAME = 'LOCAL'

    def check_before_save(self):
        super().check_before_save()
        # check dir is exists or create it
        out = self.CONFIG['OUT']
        utils.get_or_create_dir(out)

    @classmethod
    def _connect(cls):
        pass

    @classmethod
    def _close(cls):
        pass

    def _upload(self):
        out = self.CONFIG['OUT']
        file_path = self.file_path
        utils.copy_item(file_path, out)

    def _save(self):
        self.check_before_save()
        self.upload()



