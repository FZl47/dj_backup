import dropbox

from dj_backup.core import utils

from .base import BaseStorageConnector


class DropBoxConnector(BaseStorageConnector):
    CONFIG = {
        'ACCESS_TOKEN': None,
        'OUT': '/dj_backup/'
    }
    STORAGE_NAME = 'DROPBOX'
    DBX = None

    @classmethod
    def _connect(cls):
        """
            create connection to host server
        """
        c = cls.CONFIG
        dbx = dropbox.Dropbox(c['ACCESS_TOKEN'])
        cls.DBX = dbx
        return dbx

    @classmethod
    def _close(cls):
        """
            close connections
        """
        if cls.DBX: cls.DBX.close()

    def _upload(self, dbx, output):
        with open(self.file_path, 'rb') as file:
            dbx.files_upload(file.read(), output)

    def save(self):
        try:
            self.check_before_save()
            dbx = self.connect()
            file_name = self.get_file_name()
            output = utils.join_paths(self.CONFIG['OUT'], file_name)
            self.upload(dbx, output)
            self.close()
        except Exception as e:
            self.save_fail_result(e)
        else:
            self.save_result(output)
