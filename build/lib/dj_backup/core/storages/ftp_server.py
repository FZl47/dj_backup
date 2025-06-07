import warnings
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
    IMPORT_STATUS = package_imported
    CONFIG = {
        'HOST': None,
        'PORT': 21,
        'USERNAME': None,
        'PASSWORD': None,
        'OUT': None,
    }
    STORAGE_NAME = 'FTP_SERVER'
    TRANSPORT = None
    FTP = None


    @classmethod
    def set_config(cls, config):
        super().set_config(config)
        # set ftp port
        ftplib.FTP.port = cls.CONFIG['PORT']

    @classmethod
    def _connect(cls):
        """
            create connection to host server
        """
        c = cls.CONFIG
        ftp = ftplib.FTP(c['HOST'], c['USERNAME'], c['PASSWORD'])
        cls.FTP = ftp
        return ftp

    @classmethod
    def _close(cls):
        """
            close connections
        """
        if cls.FTP: cls.FTP.close()

    def _upload(self, ftp, base_output, file_name):
        with open(self.file_path, 'rb') as file:
            # move to out path
            ftp.cwd(base_output)
            # upload
            ftp.storbinary(f'STOR {file_name}', file)

    def _save(self):
        self.check_before_save()
        ftp = self.connect()
        file_name = self.get_file_name()
        base_output = self.CONFIG['OUT']
        self.upload(ftp, base_output, file_name)
        self.close()


