import warnings

from typing import Optional, Dict, Any

try:
    import ftplib

    package_imported = True
except ImportError:
    package_imported = False
    warnings.warn("""
        To use the storage provider 'FTP Server', you need to install its package; otherwise, it cannot be used.
        You can install the required package using the following command:
        'pip install djbackup[ftpserver]'""")

from .base import BaseStorageConnector


class FTPServerConnector(BaseStorageConnector):
    """
        A connector class for interacting with an FTP server.

        This class provides methods to connect to an FTP server, upload files,
        and manage configurations for FTP access.

        Attributes:
            IMPORT_STATUS (bool): Indicates whether the FTP package was imported successfully.
            CONFIG (dict): Configuration settings for FTP integration.
            STORAGE_NAME (str): Name of the storage provider.
            FTP (Optional[ftplib.FTP]): The FTP connection object.
    """

    IMPORT_STATUS: bool = package_imported
    CONFIG: Dict[str, Optional[Any]] = {
        'HOST': None,
        'PORT': 21,
        'USERNAME': None,
        'PASSWORD': None,
        'OUT': None,
    }
    STORAGE_NAME = 'FTP_SERVER'
    FTP: Optional[ftplib.FTP] = None

    @classmethod
    def set_config(cls, config: Dict[str, Any]) -> None:
        """
            Set the configuration for the FTP connection.

            :param config: A dictionary containing configuration parameters.
        """
        super().set_config(config)
        # Set FTP port
        ftplib.FTP.port = cls.CONFIG['PORT']

    @classmethod
    def _connect(cls) -> ftplib.FTP:
        """
        Create a connection to the FTP server.

        :return: An instance of the FTP connection.
        """
        c = cls.CONFIG
        ftp = ftplib.FTP(c['HOST'], c['USERNAME'], c['PASSWORD'])
        cls.FTP = ftp
        return ftp

    @classmethod
    def _close(cls) -> None:
        """
            Close the FTP connection.

            This method ensures that any open connections to the FTP server are properly closed.
        """
        if cls.FTP:
            cls.FTP.close()

    def _upload(self, ftp: ftplib.FTP, base_output: str, file_name: str) -> None:
        """
            Upload a file to the FTP server.

            :param ftp: The FTP connection object.
            :param base_output: The destination path on the FTP server where the file will be uploaded.
            :param file_name: The name of the file to be uploaded.
        """
        with open(self.file_path, 'rb') as file:
            # Move to output path
            ftp.cwd(base_output)
            # Upload the file
            ftp.storbinary(f'STOR {file_name}', file)

    def _save(self) -> None:
        """
            Save the file to the FTP server after performing necessary checks.

            This method checks conditions before saving, establishes a connection,
            uploads the file, and then closes the connection.
        """
        self.check_before_save()
        ftp = self.connect()
        file_name = self.get_file_name()
        base_output = self.CONFIG['OUT']
        self.upload(ftp, base_output, file_name)
        self.close()
