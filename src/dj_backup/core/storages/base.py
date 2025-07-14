import abc
import time

from typing import Any, Dict, Optional, Union

from pathlib import Path

from django.db.models import ObjectDoesNotExist

from dj_backup.core import utils
from dj_backup import models


class BaseStorageConnector(abc.ABC):
    STORAGE_NAME = None
    CONFIG: Dict[str, Any] = None
    IMPORT_STATUS = None
    _check_status = None
    time_taken: float = 0.0

    def __init__(self, backup_obj: Optional[Union[models.DJFileBackUp, models.DJDataBaseBackUp]] = None,
                 file_path: Optional[Union[Path, str]] = None) -> None:
        """
            Initializes the storage connector.

            :param backup_obj: The backup object associated with this storage. Can be None.
            :param file_path: The path to the file to be processed. Can be None.
                              This is to prevent errors during usage in the template.
        """
        self.backup_obj = backup_obj
        self.file_path = file_path

    def save(self) -> None:
        """
            Saves the specified file to the storage.

            This method calculates the time taken to save the file and handles both successful and
            unsuccessful save attempts. On success, it generates the output path using the configured
            output directory and the name of the file being saved. The result of the operation is then
            recorded in the database.

            If an error occurs during the save process, the failure is logged, and the failure result
            is recorded in the database.

            :raises Exception: If an error occurs during the save operation, it is caught and handled
                              by logging the failure and saving the failure result.
        """
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
    def set_config(cls, config: Dict[str, Any]) -> None:
        """
            Sets the configuration for the storage connector.

                :param config: Configuration dictionary.
                :raises AttributeError: If required fields are missing.
        """
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

    def check_before_save(self) -> None:
        """
            Checks if the necessary conditions are met before saving the file.

            This method verifies that the `file_path` attribute is set and that the file
            specified by `file_path` exists. If either condition is not met, an appropriate
            error message is logged, and an exception is raised.

            :raises AttributeError: If the `file_path` attribute is not set.
            :raises OSError: If the file specified by `file_path` does not exist.
        """
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
            utils.log_event('There is a problem in checking before save storage %s' % self.STORAGE_NAME, 'error',
                            exc_info=True)
            raise

    @classmethod
    def setup(cls) -> None:
        """
        Setup method for subclasses to implement.

        This method serves as a placeholder for any initialization or setup
        procedures that subclasses may need to perform. Subclasses should
        override this method to provide their specific setup logic.

        Note:
            This method does not perform any actions by default and should
            be implemented in subclasses as needed.
        """
        pass

    @classmethod
    def check(cls, raise_exc: bool = True) -> bool:
        """
            Checks the storage connection status.

            This method verifies whether the storage connection is active and
            functioning correctly. It attempts to connect and close the connection
            to ensure that the storage is accessible.

            :param raise_exc: If set to True, an exception will be raised on failure;
                              if False, the method will return False instead.
            :return: True if the connection check is successful, False otherwise.

            This method utilizes a cached status (`cls._check_status`) to avoid
            unnecessary checks if the status has already been determined.

            Note:
                If an error occurs during the connection check, an error message
                will be logged, and depending on the `raise_exc` parameter, an
                exception may be raised to indicate the failure.
        """
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
                Make sure the config is set correctly.
                See detail [%s]
            """ % (cls.STORAGE_NAME, e)
            utils.log_event(msg, 'error', exc_info=True)
            if raise_exc:
                raise Exception(msg)
            return False

    @classmethod
    def connect(cls, raise_exc: bool = True) -> Union[object, Exception, None]:
        """
            Handles exceptions while connecting to storage.

            This method attempts to establish a connection to the storage system.
            If the connection is successful, the connection object is returned.
            In case of failure, an error message is logged, and depending on the
            `raise_exc` parameter, an exception may be raised.

            :param raise_exc: If True, an exception will be raised on failure;
                              if False, the method will return None instead.
            :return: The connection object if the connection is successful,
                     None otherwise.
        """
        try:
            return cls._connect()
        except Exception as e:
            utils.log_event('There is a problem with %s storage connection. More info [%s]' % (cls.__name__, e),
                            'critical',
                            exc_info=True)
            if raise_exc:
                raise
        return None

    @classmethod
    def close(cls, raise_exc: bool = True) -> Union[object, Exception, None]:
        """
            Handles exceptions while closing storage connections.

            This method attempts to close the connection to the storage system.
            If the operation is successful, the result of the close operation is returned.
            In case of failure, an error message is logged, and depending on the
            `raise_exc` parameter, an exception may be raised.

            :param raise_exc: If True, an exception will be raised on failure;
                              if False, the method will return None instead.
            :return: The result of the close operation if successful, None otherwise.
        """
        try:
            return cls._close()
        except Exception as e:
            utils.log_event('There is a problem with %s storage close connections. More info [%s]' % (cls.__name__, e),
                            'error',
                            exc_info=True)
            if raise_exc:
                raise
        return None

    def upload(self, *args: Any, raise_exc: bool = True) -> Union[object, Exception, None]:
        """
            Uploads data to storage.

            This method facilitates the upload of data to the storage system.
            It accepts variable arguments that are passed to the upload operation.
            If the upload is successful, the result of the upload operation is returned.
            In case of failure, an error message is logged, and depending on the
            `raise_exc` parameter, an exception may be raised.

            :param args: Arguments for the upload method.
            :param raise_exc: If True, an exception will be raised on failure;
                              if False, the method will return None instead.
            :return: The result of the upload operation if successful, None otherwise.
        """
        try:
            return self._upload(*args)
        except Exception as e:
            utils.log_event('There is a problem with %s storage upload. More info [%s]' % (self.__class__.__name__, e),
                            'critical',
                            exc_info=True)
            if raise_exc:
                raise
        return None

    @classmethod
    @abc.abstractmethod
    def _connect(cls) -> Any:
        """Connect to the storage. Must be implemented by subclasses."""
        pass

    @classmethod
    @abc.abstractmethod
    def _close(cls) -> None:
        """Close the storage connection. Must be implemented by subclasses."""
        pass

    @abc.abstractmethod
    def _upload(self, *args: Any, **kwargs: Any) -> Any:
        """Upload data to the storage. Must be implemented by subclasses."""
        pass

    @abc.abstractmethod
    def _save(self, *args: Any, **kwargs: Any) -> None:
        """Save data to the storage. Must be implemented by subclasses."""
        pass

    @classmethod
    def get_available_of_space(cls) -> Union[float, None]:
        """Get the available space in the storage. Default is None."""
        return None

    def get_file_size(self) -> int:
        """Get the size of the file specified by file_path."""
        try:
            return utils.get_file_size(self.file_path)
        except OSError:
            utils.log_event('File `%s` does not exist or is inaccessible' % self.file_path, 'warning', exc_info=True)
            return -1

    def get_file_name(self) -> str:
        """Get the name of the file specified by file_path."""
        return utils.get_file_name(self.file_path)

    def get_storage_object(self) -> Union[models.DJStorage, Exception]:
        """Retrieve the storage object from the database."""
        obj = models.DJStorage.objects.filter(name=self.STORAGE_NAME).first()
        if not obj:
            msg = 'DJStorage object not found with `%s` name' % self.STORAGE_NAME
            utils.log_event(msg, 'warning', exc_info=True)
            raise ObjectDoesNotExist(msg)
        return obj

    def save_result(self, out: str) -> Union[models.DJBackUpStorageResult, None]:
        """Save the result of a successful operation to the database."""
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

    def save_fail_result(self, exception: Exception) -> Union[models.DJBackUpStorageResult, None]:
        """Save the result of a failed operation to the database."""
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

    def __str__(self) -> str:
        """Return the string representation of the storage connector."""
        return self.STORAGE_NAME

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the storage connector."""
        return cls.STORAGE_NAME

    def normalize_time_sec(self, time_v: float) -> float:
        """Normalize the time in seconds to two decimal places."""
        return float("%.2f" % time_v)
