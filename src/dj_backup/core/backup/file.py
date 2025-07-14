from pathlib import Path

from dj_backup import settings
from dj_backup.core import utils
from dj_backup.core.backup.base import BaseBackup


class FileBackup(BaseBackup):
    """
        The FileBackup class handles the process of creating backups of files.
        It provides functionalities to save, compress, and delete backup files.

        Attributes:
            backup_obj (object): An object responsible for managing backup details,
                                 including fetching files and backup location.
            base_dir_name (str): The temporary directory path where files are stored during backup.

        Methods:
            _get_base_dir_compress(): Returns the path to the final compressed backup ZIP file.
            _save_temp_files(): Saves the files to the temporary directory.
            save_temp(): Compresses files and creates the final ZIP backup, returning its path.
            delete_raw_temp(): Deletes the temporary file.
            delete_zip_temp(): Deletes the temporary ZIP backup file.
            _get_backup(): Executes the backup process and returns the path to the backup ZIP file.
    """

    def __init__(self, backup_obj) -> None:
        """
            Initializes the FileBackup instance.

            Args:
                backup_obj (object): The backup object that manages files and storage location.
        """
        super().__init__()
        self.backup_obj = backup_obj
        self.base_dir_name = utils.join_paths(settings.get_backup_temp_dir(), backup_obj.get_backup_location())

    def _get_base_dir_compress(self) -> Path:
        """
            Returns the path for the final ZIP file containing the backup.

            Returns:
                str: Path to the ZIP file.
        """
        return Path(f'{self.base_dir_name}.zip')

    def _save_temp_files(self) -> None:
        """
            Saves the backup files into the temporary directory.
        """
        files_obj = self.backup_obj.get_files()
        # Create directory if it doesn't exist
        utils.get_or_create_dir(self.base_dir_name)
        utils.log_event('Directory %s created' % self.base_dir_name, 'debug')
        for file_obj in files_obj:
            file_obj.save_temp(self.base_dir_name)

    def save_temp(self) -> Path:
        """
            Compresses the files, creating the backup ZIP archive.

            Returns:
                str: The path to the created ZIP file.

            Raises:
                Exception: If there is an issue during file compression or saving.
        """
        utils.log_event('Create temp file started..', 'debug')
        try:
            self._save_temp_files()
            utils.zip_item(self.base_dir_name, self._get_base_dir_compress())
        except Exception:
            msg = 'There is some problem in save_temp FileBackup'
            utils.log_event(msg, 'error', exc_info=True)
            raise
        utils.log_event("Temp files 'FileBackup' created!", 'debug')
        return self._get_base_dir_compress()

    def delete_raw_temp(self) -> None:
        """
            Deletes the temporary files stored in the initial directory.
        """
        b = self.base_dir_name
        try:
            utils.delete_item(b)
            utils.log_event('Temp file `%s` deleted successfully!' % b, 'debug')
        except (OSError, TypeError):
            utils.log_event('Some problem in delete temp file `%s`' % b, 'warning', exc_info=True)

    def delete_zip_temp(self) -> None:
        """
            Deletes the final ZIP backup file.
        """
        b = self._get_base_dir_compress()
        try:
            utils.delete_item(b)
            utils.log_event('Temp zip file `%s` deleted successfully!' % b, 'debug')
        except (OSError, TypeError):
            utils.log_event('Some problem in delete temp zip file `%s`' % b, 'warning', exc_info=True)

    def _get_backup(self) -> Path:
        """
            Executes the backup process, creating the ZIP file and returning its path.

            Returns:
                str: The path to the backup ZIP file.
        """
        return self.save_temp()
