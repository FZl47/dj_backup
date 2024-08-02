import abc
import paramiko

from dj_backup import settings
from dj_backup.core import utils

paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE = pow(2, 22)  # 4MB per chunk


class BaseStorage(abc.ABC):
    STORAGE_NAME = None
    CONFIG = None

    def __init__(self, file_path):
        self.file_path = file_path

    @abc.abstractmethod
    def save(self):
        raise NotImplementedError

    @classmethod
    def set_config(cls, config):
        for ck, cv in cls.CONFIG.items():
            try:
                config_val = config[ck]
            except KeyError:
                if not cv:
                    raise AttributeError('You should define field'
                                         ' `%s` in `%s` '
                                         'storage config' % (ck, cls.STORAGE_NAME))
                config_val = cv
            cls.CONFIG[ck] = config_val

    @classmethod
    def check(cls, raise_exc=True):
        # TODO: add log
        try:
            cls._connect()
            cls._close()
            return True
        except Exception as e:
            if raise_exc:
                raise Exception('The `%s` storage check encountered an error.'
                                ' make sure the config are set correctly.'
                                ' see detail [%s]' % (cls.STORAGE_NAME, e))
            # TODO: add log exception
            return False

    @classmethod
    def _connect(cls):
        pass

    @classmethod
    def _close(cls):
        pass


class LocalStorage(BaseStorage):
    CONFIG = {
        'OUT': None,
    }
    STORAGE_NAME = 'LOCAL'

    def save(self):
        out = self.CONFIG['OUT']
        utils.copy_item(self.file_path, out)


class BasicServerStorage(BaseStorage):
    CONFIG = {
        'HOST': None,
        'PORT': 22,
        'USERNAME': None,
        'PASSWORD': None,
        'OUT': None,
    }
    STORAGE_NAME = 'BASIC_SERVER'
    TRANSPORT = None
    SFTP = None

    @classmethod
    def _connect(cls):
        """
            create connection to host server
        """
        # TODO: add custom exception handler
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

    def save(self):
        # TODO: add exception handler
        transport, sftp = self._connect()
        file_name = utils.get_file_name(self.file_path)
        output = utils.join_paths(self.CONFIG['OUT'], file_name).replace(' ', '-')
        sftp.put(self.file_path, output)
        self._close()


_STORAGES = {
    'LOCAL': LocalStorage,
    'BASIC_SERVER': BasicServerStorage,
}

STORAGES_AVAILABLE = []


def _get_storages_available():
    storages_config = settings.get_storages_config()
    for st_name, st_config in storages_config.items():
        try:
            storage_cls = _STORAGES[st_name]
        except KeyError:
            raise ValueError('Unknown `%s` storage' % st_name)

        storage_cls.set_config(st_config)
        if storage_cls.check():
            STORAGES_AVAILABLE.append(storage_cls)


_get_storages_available()
