import paramiko

from dj_backup.core import utils

from .base import BaseStorageConnector


class SFTPServerConnector(BaseStorageConnector):
    # paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE = pow(2, 22)  # 4MB per chunk
    CONFIG = {
        'HOST': None,
        'PORT': 22,
        'USERNAME': None,
        'PASSWORD': None,
        'OUT': None,
    }
    STORAGE_NAME = 'SFTP_SERVER'
    TRANSPORT = None
    SFTP = None

    @classmethod
    def _connect(cls):
        """
            create connection to host server
        """
        c = cls.CONFIG
        transport = paramiko.Transport((c['HOST'], c['PORT']))
        transport.connect(username=c['USERNAME'], password=c['PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        cls.TRANSPORT = transport
        cls.SFTP = sftp
        return transport, sftp

    @classmethod
    def _close(cls):
        """
            close connections
        """
        if cls.SFTP: cls.SFTP.close()
        if cls.TRANSPORT: cls.TRANSPORT.close()

    def _upload(self, sftp, output):
        sftp.put(self.file_path, output)

    def _save(self):
        self.check_before_save()
        transport, sftp = self.connect()
        file_name = self.get_file_name()
        output = utils.join_paths(self.CONFIG['OUT'], file_name)
        self.upload(sftp, output)
        self.close()


