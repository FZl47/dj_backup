import pyzipper
import os

from typing import Union
from pathlib import Path

from dj_backup.core.utils import log_event

from . import SecureBaseABC


class ZipPassword(SecureBaseABC):
    """
         A class for implementing secure backup by zipping files with password encryption.
    """

    def save(self, directory_or_file: Path, zip_file: Path, key: str) -> Union[Path, None]:
        """
            Get encrypted content and save
            In this case, there is no need to save it again because it is saved during encryption.

            :param directory_or_file: The path of a file or directory.
            :param zip_file: The name of the output zip file (should include .zip extension).
            :param key: A string representing the encryption key or password.

            :return: Encrypted zip file(replace new encrypted file with old file).
        """
        try:
            return self.encrypt(directory_or_file, zip_file, key)
        except OSError:
            return None

    def encrypt(self, directory_or_file: Path, zip_file: Path, key: str) -> Path:
        """
            Encrypts file or directory.

            :param directory_or_file: The path of a file or directory.
            :param zip_file: The name of the output zip file (should include .zip extension).
            :param key: A string representing the encryption key or password.

            :return: Encrypted zip file.
        """
        log_event('encryption zipp started.', 'debug')

        if os.path.isdir(directory_or_file):
            self._zp_directory(directory_or_file, zip_file, key)
        else:
            self._zp_file(directory_or_file, zip_file, key)

        log_event('encryption zipp has done.', 'debug')

        return zip_file

    def decrypt(self, zip_file: Path, key: str) -> Path:
        """
            Decrypts the given file.

            :param zip_file: A zip file object to be decrypted.
            :param key: A string representing the decryption key or password.

            :return: The decrypted file object, which may be in a different format than the original file.
        """

        log_event('decryption zipp started.', 'debug')

        zip_file_without_extension = str(zip_file).split('.')[0]
        ex = '%s_extracted' % zip_file_without_extension
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = key
            zf.extractall(ex)

        log_event('decryption zipp has done.', 'debug')

        return Path(ex)

    @classmethod
    def _zp_directory(cls, directory: Path, zip_file: Path, key: str) -> None:
        """
           Creates a zip file from the specified directory.

           :param directory: The Path object representing the directory to be zipped.
           :param zip_file: The name of the output zip file (should include .zip extension).
           :param key: A string representing the encryption key or password.
        """

        with pyzipper.AESZipFile(zip_file, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
            # set password
            zipf.setpassword(key)
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=directory)
                    zipf.write(file_path, arcname=arcname)

    @classmethod
    def _zp_file(cls, file_path: Path, zip_file: Path, key: str) -> None:
        """
           Creates a zip file from the specified file.

           :param file_path: The Path object representing the file to be zipped.
           :param zip_file: The name of the output zip file (should include .zip extension).
           :param key: A string representing the encryption key or password.
        """
        with pyzipper.AESZipFile(zip_file, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
            # set password
            zipf.setpassword(key)
            zipf.write(file_path, arcname=os.path.basename(file_path))
