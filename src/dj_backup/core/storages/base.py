import abc

from django.db.models import ObjectDoesNotExist

from dj_backup.core import utils
from dj_backup import models


class BaseStorageConnector(abc.ABC):
    STORAGE_NAME = None
    CONFIG = None
    _check_status = None

    def __init__(self, backup_obj=None, file_path=None):
        """
            file_path or backup_obj can be None. to prevent errors during usage in the template.
        """
        self.backup_obj = backup_obj
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

    def check_before_save(self):
        try:
            file_path = getattr(self, 'file_path', None)
            if not file_path:
                msg = 'You must set `file_path` attribute'
                utils.log_event(msg, 'error')
                raise AttributeError(msg)
            if not utils.file_is_exists(file_path):
                msg = 'File `%s` does not exist' % file_path
                utils.log_event(msg, 'error')
                raise OSError(msg)
        except (AttributeError, OSError):
            utils.log_event('There is problem in checking before save storage %s' % self.STORAGE_NAME, 'error',
                            exc_info=True)
            raise

    @classmethod
    def check(cls, raise_exc=True):
        if cls._check_status:
            return cls._check_status
        utils.log_event('Storages checking started..!', 'debug')
        try:
            cls._connect()
            cls._close()
            cls._check_status = True
            return True
        except Exception as e:
            cls._check_status = False
            msg = """
                The `%s` storage check encountered an error.
                make sure the config are set correctly.
                see detail [%s]
            """ % (cls.STORAGE_NAME, e)
            utils.log_event(msg, 'error', exc_info=True)
            if raise_exc:
                raise Exception(msg)
            return False

    @classmethod
    def connect(cls, raise_exc=True):
        """
            handle exceptions
        """
        try:
            return cls._connect()
        except Exception as e:
            utils.log_event('There is a problem with %s storage connection. more info [%s]' % (cls.__name__, e),
                            'critical',
                            exc_info=True)
            if raise_exc:
                raise
        return None

    @classmethod
    def close(cls, raise_exc=True):
        """
            handle exceptions
         """
        try:
            return cls._close()
        except Exception as e:
            utils.log_event('There is a problem with %s storage close connections. more info [%s]' % (cls.__name__, e),
                            'critical',
                            exc_info=True)
            if raise_exc:
                raise
        return None

    def upload(self, *args, raise_exc=True):
        try:
            return self._upload(*args)
        except Exception as e:
            utils.log_event('There is a problem with %s storage upload. more info [%s]' % (self.__class__.__name__, e),
                            'critical',
                            exc_info=True)
            if raise_exc:
                raise
        return None

    @classmethod
    @abc.abstractmethod
    def _connect(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def _close(cls):
        pass

    @abc.abstractmethod
    def _upload(self, *args, **kwargs):
        pass

    @classmethod
    def get_available_of_space(cls):
        return None

    def get_file_size(self):
        try:
            return utils.get_file_size(self.file_path)
        except OSError:
            utils.log_event('File `%s` does not exist or is inaccessible' % self.file_path, 'warning', exc_info=True)
            return 0

    def get_file_name(self):
        return utils.get_file_name(self.file_path)

    def get_storage_object(self):
        obj = models.DJStorage.objects.filter(name=self.STORAGE_NAME).first()
        if not obj:
            msg = 'DJStorage object not found with `%s` name' % self.STORAGE_NAME
            utils.log_event(msg, exc_info=True)
            raise ObjectDoesNotExist(msg)
        return obj

    def save_result(self, out):
        try:
            st_obj = self.get_storage_object()
            result = models.DJBackUpStorageResult.objects.create(
                status='successful',
                storage=st_obj,
                backup_name=self.get_file_name(),
                out=out,
                temp_location=self.file_path,
                size=self.get_file_size(),
            )
            self.backup_obj.results.add(result)
            return result
        except ObjectDoesNotExist:
            pass

    def save_fail_result(self, exception):
        try:
            st_obj = self.get_storage_object()
            result = models.DJBackUpStorageResult.objects.create(
                status='unsuccessful',
                storage=st_obj,
                backup_name=self.get_file_name(),
                size=self.get_file_size(),
                temp_location=self.file_path,
                description=str(exception)
            )
            self.backup_obj.results.add(result)
            return result
        except ObjectDoesNotExist:
            pass

    def __str__(self):
        return self.STORAGE_NAME

    @classmethod
    def get_name(cls):
        return cls.STORAGE_NAME
