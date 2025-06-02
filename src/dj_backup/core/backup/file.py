from dj_backup import settings
from dj_backup.core import utils
from dj_backup.core.backup.base import BaseBackup


class FileBackup(BaseBackup):

    def __init__(self, backup_obj):
        super().__init__()
        self.backup_obj = backup_obj
        self.base_dir_name = utils.join_paths(settings.get_backup_temp_dir(), backup_obj.get_backup_location())

    def _get_base_dir_compress(self):
        return f'{self.base_dir_name}.zip'

    def _save_temp_files(self):
        files_obj = self.backup_obj.get_files()
        # create base dir(self backup direction)
        utils.get_or_create_dir(self.base_dir_name)
        utils.log_event('Directory %s created' % self.base_dir_name, 'debug')
        for file_obj in files_obj:
            file_obj.save_temp(self.base_dir_name)

    def save_temp(self):
        """
            save temporary file(zip)
        """
        utils.log_event('Create temp file started..', 'debug')
        try:
            self._save_temp_files()
            utils.zip_item(self.base_dir_name, self._get_base_dir_compress())
        except Exception:
            msg = 'There is some problem in save_temp FileBackup'
            utils.log_event(msg, 'error', exc_info=True)
            raise
        utils.log_event("Temp files 'FileBackup' created !", 'debug')
        return self._get_base_dir_compress()

    def delete_raw_temp(self):
        # delete raw file
        b = self.base_dir_name
        try:
            utils.delete_item(b)
            utils.log_event('Temp file `%s` deleted successfully!' % b, 'debug')
        except OSError:
            utils.log_event('Some problem in delete temp file `%s`' % b, 'warning', exc_info=True)

    def _get_backup(self):
        return self.save_temp()
