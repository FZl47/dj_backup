from dj_backup import settings

from .local import LocalStorageConnector
from .ftp_server import FTPServerConnector
from .sftp_server import SFTPServerConnector
from .drop_box import DropBoxConnector

ALL_STORAGES_DICT = {
    'LOCAL': LocalStorageConnector,
    'SFTP_SERVER': SFTPServerConnector,
    'FTP_SERVER': FTPServerConnector,
    'DROPBOX': DropBoxConnector,
}
STORAGES_AVAILABLE = []


def _get_storages_available():
    storages_config = settings.get_storages_config()
    for st_name, st_config in storages_config.items():
        try:
            storage_cls = ALL_STORAGES_DICT[st_name]
        except KeyError:
            raise ValueError('Unknown `%s` storage' % st_name)

        storage_cls.set_config(st_config)
        if storage_cls.check():
            STORAGES_AVAILABLE.append(storage_cls)


_get_storages_available()
