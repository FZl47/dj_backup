from typing import Dict, Any, Optional

from dj_backup.core import utils

from .base import BaseStorageConnector


class LocalStorageConnector(BaseStorageConnector):
    """
        A connector class for local storage operations.

        This class provides methods to check the directory, upload files
        to a local path, and manage configurations for local storage.

        Attributes:
            CONFIG (dict): Configuration settings for local storage.
            STORAGE_NAME (str): Name of the storage provider.
    """

    CONFIG: Dict[str, Optional[Any]] = {
        'OUT': None,
    }
    STORAGE_NAME = 'LOCAL'

    def check_before_save(self) -> None:
        """
            Check if the output directory exists; if not, create it.

            This method ensures that the specified output directory is available
            before attempting to save any files.
        """
        super().check_before_save()
        out = self.CONFIG['OUT']
        utils.get_or_create_dir(out)

    @classmethod
    def _connect(cls) -> None:
        """
            Establish a connection to the local storage.

            This method is a placeholder since local storage does not require
            a connection like remote storage systems.
        """
        pass

    @classmethod
    def _close(cls) -> None:
        """
            Close the connection to local storage.

            This method is a placeholder since local storage does not require
            a connection to be closed.
        """
        pass

    def _upload(self) -> None:
        """
            Upload a file to the local storage.

            This method copies the file from the source path to the specified
            output directory.

            :raises FileNotFoundError: If the file to upload does not exist.
        """
        out = self.CONFIG['OUT']
        file_path = self.file_path
        utils.copy_item(file_path, out)

    def _save(self) -> None:
        """
            Save the file to local storage after performing necessary checks.

            This method checks conditions before saving and then uploads the file.
        """
        self.check_before_save()
        self.upload()
