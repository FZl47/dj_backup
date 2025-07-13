import abc
import time

from django.db.models import ObjectDoesNotExist

from dj_backup.core import utils
from dj_backup import models


class BaseStorageConnector(abc.ABC):
    STORAGE_NAME = None
    CONFIG = None
    IMPORT_STATUS = None
    _check_status = None
    time_taken = 0

    def __init__(self, backup_obj=None, file_path=None):
        """
            file_path or backup_obj can be None. to prevent errors during usage in the template.
        """
        self.backup_obj = backup_obj
        self.file_path = file_path

    def save(self):
        # calc time taken
        _st = time.time()
        try:
            self._save()
            self.time_taken += time.time() - _st
            output = utils.join_paths(self.CONFIG['OUT'], self.get_file_name())
            self.save_result(output)
        except Exception as e:
            self.time_taken += time.time() - _st
            self.save_fail_result(e)

    @classmethod
    def set_config(cls, config):
        for ck, cv in cls.CONFIG.items():
            try:
                config_val = config[ck]
            except KeyError:
                if not cv:
                    raise AttributeError('You should set field'
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
    def setup(cls):
        pass

    @classmethod
    def check(cls, raise_exc=True):
        if cls._check_status:
            return cls._check_status
        if cls.IMPORT_STATUS is False:
            return False
        utils.log_event('Storage [%s] checking started..!' % cls.STORAGE_NAME, 'debug')
        try:
            cls._connect()
            cls._close()
            cls._check_status = True
            utils.log_event('Storage [%s] checked successfully!' % cls.STORAGE_NAME, 'debug')
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
                            'error',
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

    @abc.abstractmethod
    def _save(self, *args, **kwargs):
        pass

    @classmethod
    def get_available_of_space(cls):
        return None

    def get_file_size(self):
        try:
            return utils.get_file_size(self.file_path)
        except OSError:
            utils.log_event('File `%s` does not exist or is inaccessible' % self.file_path, 'warning', exc_info=True)
            return -1

    def get_file_name(self):
        return utils.get_file_name(self.file_path)

    def get_storage_object(self):
        obj = models.DJStorage.objects.filter(name=self.STORAGE_NAME).first()
        if not obj:
            msg = 'DJStorage object not found with `%s` name' % self.STORAGE_NAME
            utils.log_event(msg, 'warning', exc_info=True)
            raise ObjectDoesNotExist(msg)
        return obj

    def save_result(self, out):
        try:
            st_obj = self.get_storage_object()
        except ObjectDoesNotExist:
            return None

        result = models.DJBackUpStorageResult.objects.create(
            status='successful',
            storage=st_obj,
            backup_name=self.get_file_name(),
            out=out,
            time_taken=self.normalize_time_sec(self.time_taken),
            temp_location=self.file_path,
            size=self.get_file_size(),
        )
        self.backup_obj.results.add(result)
        return result

    def save_fail_result(self, exception):
        try:
            st_obj = self.get_storage_object()
        except ObjectDoesNotExist:
            return None

        result = models.DJBackUpStorageResult.objects.create(
            status='unsuccessful',
            storage=st_obj,
            backup_name=self.get_file_name(),
            size=self.get_file_size(),
            time_taken=self.normalize_time_sec(self.time_taken),
            temp_location=self.file_path,
            description=str(exception)
        )
        self.backup_obj.results.add(result)
        return result

    def __str__(self):
        return self.STORAGE_NAME

    @classmethod
    def get_name(cls):
        return cls.STORAGE_NAME

    def normalize_time_sec(self, time):
        return float("%.2f" % time)
