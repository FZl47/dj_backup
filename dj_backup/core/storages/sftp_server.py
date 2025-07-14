import warnings

from typing import Optional, Tuple, Dict, Any

try:
    import paramiko

    package_imported = True
except ImportError:
    package_imported = False
    warnings.warn("""
        To use the storage provider 'SFTP Server', you need to install its package; otherwise, it cannot be used.
        You can install the required package using the following command:
        'pip install djbackup[sftpserver]'""")

from dj_backup.core import utils

from .base import BaseStorageConnector


class SFTPServerConnector(BaseStorageConnector):
    """
        A connector class for interacting with an SFTP server.

        This class provides methods to connect to an SFTP server, upload files,
        and manage configurations for SFTP access.

        Attributes:
            IMPORT_STATUS (bool): Indicates whether the SFTP package was imported successfully.
            CONFIG (dict): Configuration settings for SFTP integration.
            STORAGE_NAME (str): Name of the storage provider.
            TRANSPORT (Optional[paramiko.Transport]): The transport connection object.
            SFTP (Optional[paramiko.SFTPClient]): The SFTP client object.
    """

    IMPORT_STATUS: bool = package_imported
    CONFIG: Dict[str, Optional[Any]] = {
        'HOST': None,
        'PORT': 22,
        'USERNAME': None,
        'PASSWORD': None,
        'OUT': None,
    }
    STORAGE_NAME: str = 'SFTP_SERVER'
    TRANSPORT: Optional[paramiko.Transport] = None
    SFTP: Optional[paramiko.SFTPClient] = None

    @classmethod
    def _connect(cls) -> Tuple[paramiko.Transport, paramiko.SFTPClient]:
        """
            Create a connection to the SFTP server.

            :return: A tuple containing the transport and SFTP client objects.
        """
        c = cls.CONFIG
        transport = paramiko.Transport((c['HOST'], c['PORT']))
        transport.connect(username=c['USERNAME'], password=c['PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        cls.TRANSPORT = transport
        cls.SFTP = sftp
        return transport, sftp

    @classmethod
    def _close(cls) -> None:
        """
            Close the SFTP and transport connections.

            This method ensures that any open connections to the SFTP server are properly closed.
        """
        if cls.SFTP:
            cls.SFTP.close()
        if cls.TRANSPORT:
            cls.TRANSPORT.close()

    def _upload(self, sftp: paramiko.SFTPClient, output: str) -> None:
        """
            Upload a file to the SFTP server.

            :param sftp: The SFTP client object.
            :param output: The destination path on the SFTP server where the file will be uploaded.
        """
        sftp.put(self.file_path, output)

    def _save(self) -> None:
        """
            Save the file to the SFTP server after performing necessary checks.

            This method checks conditions before saving, establishes a connection,
            uploads the file, and then closes the connection.
        """
        self.check_before_save()
        transport, sftp = self.connect()
        file_name = self.get_file_name()
        output = utils.join_paths(self.CONFIG['OUT'], file_name)
        self.upload(sftp, output)
        self.close()
