from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .file.utils import zip_item, get_location, get_or_create_dir, delete_file, copy_item


class FileBackup:

    def __init__(self, file_path, file_save_path=None):
        self.location = get_location(file_path)
        self.file_save_path = file_save_path
        # TODO: add datetime on name file
        self._temp_name = f'{self.get_backup_temp_dir()}/{self.location.name}.zip'

    @classmethod
    def get_backup_dirs(cls):
        return settings.DJ_BACKUP_CONFIG['BACKUP_DIRS']

    @classmethod
    def get_backup_temp_dir(cls):
        return settings.DJ_BACKUP_CONFIG['BACKUP_TEMP_DIR']

    @classmethod
    def create_backup_dirs(cls):
        # TODO: better run in start command
        # create backup temp dir
        get_or_create_dir(cls.get_backup_temp_dir())
        # create backup root dirs
        for d in cls.get_backup_dirs():
            get_or_create_dir(d)

    def save(self):
        # TODO: save by config => self config | base config
        self._save_by_zip()

    def _save_temp(self):
        zip_item(self.location, self._temp_name)

    def _delete_temp(self):
        delete_file(self._temp_name)

    def _save_by_zip(self):
        self._save_temp()
        for d in self.get_backup_dirs():
            copy_item(self._temp_name, d)
        self._delete_temp()


__all__ = ['FileBackup']
