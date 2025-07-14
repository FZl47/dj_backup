from abc import ABC
from pathlib import Path
from typing import Any

from dj_backup.core import utils


class SecureBaseABC(ABC):
    """
        A base class for implementing secure backup mechanisms.

        This class provides an interface for creating secure backup.
        It requires subclasses to implement the encryption and decryption methods,
        ensuring that any backup object can be securely processed.

        Attributes:
            _prefix_out: new path of encrypted backup:
                {_prefix_out}_backup_name.zip
            enc_file_out:
                encrypted new file path
    """
    _prefix_out = None
    enc_file_out = None

    def delete_temp_files(self) -> None:
        """
            Delete temp files
        """
        # delete zip file
        b = self.enc_file_out
        try:
            utils.delete_item(b)
            utils.log_event('Encrypted temp zip file `%s` deleted successfully!' % b, 'debug')
        except (OSError, TypeError):
            utils.log_event('Some problem in delete encrypted temp zip file `%s`' % b, 'warning', exc_info=True)

    def save(self, *args, **kwargs) -> Path:
        """
            Must be implemented in subclass.

            get encrypt content and save
        """
        raise NotImplementedError

    def encrypt(self, *args, **kwargs) -> Any:
        """
            Must be implemented in subclass.
        """
        raise NotImplementedError

    def decrypt(self, *args, **kwargs) -> Any:
        """
            Must be implemented in subclass.
        """
        raise NotImplementedError

    def _get_out_filename(self, filename: Path) -> Path:
        """
            :param filename: The name of the file that needs to be encrypted.

            :return: Path of new file(encrypted)
        """

        last_dir_name = filename.name
        new_dir_name = self._prefix_out + last_dir_name
        filename_new_path = filename.parent / new_dir_name
        return filename_new_path

