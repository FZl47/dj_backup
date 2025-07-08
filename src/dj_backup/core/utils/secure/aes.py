import hashlib

from typing import Union
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from dj_backup.core import utils, logging
from dj_backup import settings

from . import SecureBaseABC


class AESEncryption(SecureBaseABC):
    """
        A class for implementing secure backup by AES-256 encryption.

        Attributes:
            _save_prefix:
                it used when we want to make encrypted file: {_save_prefix}_backup.zip
            _file_extension:
                {_save_prefix}_backup.{_file_extension}
    """
    _save_prefix = 'enc'
    _file_extension = 'bin'

    temp_dir = settings.get_backup_temp_dir()

    @property
    def temp_encrypt_data_loc(self) -> Path:
        """
            :return: A path of temp location to save encrypted data
        """
        return self.temp_dir / utils.random_str(20) / 'bc.%s' % self._file_extension

    @classmethod
    def _make_key_sha256(cls, key: str) -> bytes:
        """
            Get key and made sha256 hash

            :param key: A string representing the encryption key

            :return: Bytes sha256(digest)
        """
        return hashlib.sha256(key.encode('utf-8')).digest()

    def _save_temp_encrypted_data(self, encrypted_data: bytes) -> Path:
        """
            Save temporary encrypted data

            :return: temp file
        """
        loc = self.temp_encrypt_data_loc
        with open(loc, 'wb') as f:
            f.write(encrypted_data)
        logging.log_event('file temp encrypted created', 'debug')
        return loc

    def _delete_temp_encrypted_data(self, temp_encrypted_file: Path) -> None:
        """
            Delete temporary encrypted data
        """
        try:
            utils.delete_item(temp_encrypted_file)
            logging.log_event('file temp encrypted deleted', 'debug')
        except OSError:
            logging.log_event('error in delete temp encrypted file', 'warning', exc_info=True)

    def save(self, filename: Path, key: str) -> Union[Path, None]:
        """
            Get encrypt content and save

            :param filename: The name of the file that needs to be encrypted.
            :param key: A string representing the encryption key or password.

            :return: The encrypted content as file(replace new encrypted file with old file).
        """
        encrypted_data = self.encrypt(filename, key)
        # create encrypted file
        enc_file = self._save_temp_encrypted_data(encrypted_data)

        # zip encrypted file
        try:
            utils.zip_file(enc_file, filename)
        except (IOError, TypeError):
            logging.log_event('error in zip encrypted file', 'warning', exc_info=True)
            return None

        # delete temp encrypted file
        self._delete_temp_encrypted_data(enc_file)

        logging.log_event('encrypt file maked success', 'warning', exc_info=True)
        return filename

    def encrypt(self, filename: Path, key: str) -> bytes:
        """
            Encrypts the given file and returns the encrypted content.

            :param filename: The name of the file that needs to be encrypted.
            :param key: A string representing the encryption key or password.

            :return: The encrypted file as bytes.
        """

        # read the zip file
        with open(filename, 'rb') as f:
            data = f.read()

        skey = self._make_key_sha256(key).decode('utf-8')

        # encrypt the data
        cipher = AES.new(skey, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))

        # combine the IV with the ciphertext
        iv = cipher.iv
        encrypted_data = iv + ct_bytes

        return encrypted_data

    def decrypt(self, encrypted_data: bytes, key: str) -> bytes:
        """
            Decrypts the given encrypted content.

            :param encrypted_data: The encrypted content to be decrypted.
            :param key: A string representing the decryption key.
            :return: The decrypted content as bytes.
        """

        # extract the IV and ciphertext
        iv = encrypted_data[:16]  # first 16 bytes are the IV
        ct = encrypted_data[16:]  # the rest is the ciphertext

        # decrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)

        return decrypted_data
