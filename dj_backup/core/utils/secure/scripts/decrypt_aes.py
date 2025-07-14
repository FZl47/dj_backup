import zipfile
import hashlib
import os
import pathlib
import getpass

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BLUE_BOLD = "\033[1;34m"
G_BOLD = "\033[1;32m"
RESET = "\033[0m"

folder_path = pathlib.Path(__file__).parent

_output = './decrypted_backup.zip'


class Decryptor:

    def decrypt(self, encrypted_data: bytes, key: str) -> bytes:
        """
            Decrypts the given encrypted content.

            :param encrypted_data: The encrypted content to be decrypted.
            :param key: A string representing the decryption key (must be 32 bytes for AES-256).
            :return: The decrypted content as bytes.
        """
        # Ensure the key is 32 bytes long

        key = self._make_key_sha256(key)

        if len(key) != 32:
            raise ValueError("Key must be 32 bytes long for AES-256.")

        # Extract the IV and ciphertext
        iv = encrypted_data[:16]  # First 16 bytes are the IV
        ct = encrypted_data[16:]  # The rest is the ciphertext

        # Decrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)

        return decrypted_data

    @classmethod
    def _make_key_sha256(cls, key: str) -> bytes:
        """
            Get key and made sha256 hash

            :param key: A string representing the encryption key

            :return: Bytes sha256(digest)
        """
        return hashlib.sha256(key.encode('utf-8')).digest()

    def load_from_zip(self, input_zip: str) -> bytes:
        """
            Loads the encrypted data from the zip file.

            :param input_zip: The name of the zip file containing the encrypted data.
            :return: The encrypted content as bytes.
        """

        with zipfile.ZipFile(input_zip, 'r') as zip_file:
            file_names = zip_file.namelist()
            file_name = file_names[0]
            encrypted_data = zip_file.read(file_name)
        return encrypted_data


def find_backup_file():
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            s = os.path.join(root, file)
            if not s == __file__:
                return s
    raise FileNotFoundError('Backup not found')


if __name__ == '__main__':
    decryptor = Decryptor()

    print(f"{BLUE_BOLD}--- Decryption Started ! ---{RESET}")

    loaded_encrypted_content = decryptor.load_from_zip(find_backup_file())

    _key = getpass.getpass('Please Enter Aes Key...')

    try:
        decrypted_content = decryptor.decrypt(loaded_encrypted_content, _key)
    except Exception as e:
        raise Exception('Key is wrong!')

    with open(_output, 'wb') as f:
        f.write(decrypted_content)

    print(f"{G_BOLD}--- Decryption File Created in '{folder_path / _output}' ! ---{RESET}")

    print(f"{G_BOLD}--- Decryption Finished Successfully ! ---{RESET}")
