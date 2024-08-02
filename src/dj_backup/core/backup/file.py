from dj_backup import settings
from dj_backup.core import utils
from dj_backup import models


class FileBackup:

    def __init__(self, backup_obj: models.DJFileBackUp):
        self.backup_obj = backup_obj
        # self.base_dir_name = f'{settings.get_backup_temp_dir()}/backup_files_{self.backup_obj.name}-{utils.get_time()}'
        self.base_dir_name = utils.join_paths(settings.get_backup_temp_dir(),
                                              f'backup_files_{self.backup_obj.name}-{utils.get_time()}')

    def _get_base_dir_compress(self):
        return f'{self.base_dir_name}.zip'

    def _save_temp_files(self):
        files_obj = self.backup_obj.get_files()
        # create base dir(self backup direction)
        utils.get_or_create_dir(self.base_dir_name)
        for file_obj in files_obj:
            file_obj.save_temp_compress(self.base_dir_name)

    def save_temp(self):
        """
            save temporary file(zip)
        """
        # TODO: add log | add handle exception
        self._save_temp_files()
        utils.zip_item(self.base_dir_name, self._get_base_dir_compress())
        return self._get_base_dir_compress()

    def delete_temp(self):
        # TODO: add log | add handle exception
        # delete compress file
        utils.delete_file(self._get_base_dir_compress())
        utils.delete_file(self.base_dir_name)


__all__ = ['FileBackup']
