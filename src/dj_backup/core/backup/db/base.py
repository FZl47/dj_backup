import abc

from typing import Dict, Union

from pathlib import Path

from dj_backup.core import utils
from dj_backup import settings
from dj_backup.core.backup.base import BaseBackup


class BaseDB(BaseBackup):
    """
        Base class for database backup functionality.

        This class provides a template for creating database backup implementations.
        It handles configuration, export location management, and provides methods for
        connecting to the database, preparing commands, and dumping data.

        Attributes:
            IMPORT_STATUS (bool): Status of the import operation.
            NAME (str): Name of the database.
            CMD (str): Command string for the backup operation.
            CONFIG_NAME (str): Name of the configuration.
            CONFIG (dict): Configuration settings for the database.
            OUTPUT_FORMAT (str): Format of the output dump file.
            DUMP_PREFIX (str): Prefix for the dump files.
            ADDITIONAL_ARGS_NAME (dict): Additional arguments' names for the command.
            ADDITIONAL_ARGS (dict): Additional arguments for the command.
            _check_status (bool): Status of the last check operation.
            export_location (str): Location where the backup will be exported.

        Args:
            backup_obj (Optional[object]): An optional object that contains backup details.
    """

    IMPORT_STATUS = None
    NAME = None
    CMD = None
    CONFIG_NAME = None
    CONFIG = None
    OUTPUT_FORMAT = 'sql'
    DUMP_PREFIX = None
    ADDITIONAL_ARGS_NAME = {}
    ADDITIONAL_ARGS = {}

    _check_status = None
    export_location = None

    def __init__(self, backup_obj=None):
        """
            Initializes the BaseDB instance.

            Args:
                backup_obj (Optional[object]): An optional object that contains backup details.
        """
        super().__init__()
        self.backup_obj = backup_obj
        if backup_obj:
            self.export_location = self._get_export_location()
            self.normalized_export_location = self.normalize_location(self.export_location)

    def _get_export_location(self) -> Path:
        """
            Retrieves the export location for the backup.

            Returns:
                Path: The path where the backup will be exported.
        """
        temp_dir = settings.get_backup_temp_dir()
        return utils.join_paths(temp_dir, self.backup_obj.get_backup_location(self.OUTPUT_FORMAT))

    def get_exp_compress_file_location(self) -> Path:
        """
        Gets the location of the compressed export file.

        Returns:
            Path: The path of the compressed export file.
        """
        return Path(f'{self.export_location}.zip')

    @classmethod
    def set_config(cls, config: Dict[str, str]):
        """
            Sets the configuration for the database.

            Args:
                config (Dict): A dictionary containing configuration settings.

            Raises:
                AttributeError: If a required configuration field is missing.
        """
        for ck, cv in cls.CONFIG.items():
            try:
                config_val = config[ck]
            except KeyError:
                if not cv:
                    raise AttributeError('You should define field'
                                         ' `%s` in `%s` '
                                         'database config' % (ck, cls.NAME))
                config_val = cv
            cls.CONFIG[ck] = config_val

    @classmethod
    def set_config_name(cls, name: str):
        """
            Sets the configuration name for the database.

            Args:
                name (str): The name of the configuration.
        """
        cls.CONFIG_NAME = name

    @classmethod
    @abc.abstractmethod
    def connect(cls):
        """
            Connects to the database.

            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def close(cls):
        """
            Closes the connection to the database.

            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def prepare_cmd(self):
        """
            Prepares the command for the backup operation.

            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self):
        """
            Executes the dump operation for the database.

            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete_dump_file(self) -> None:
        """
            Deletes the temporary dump file.

            Logs a message indicating success or failure of the deletion.
        """
        exp_loc = self.export_location
        try:
            utils.delete_item(exp_loc)
            utils.log_event(
                'Temp dump file `%s` from `%s` db deleted successfully!' % (exp_loc, self.__class__.__name__), 'debug')
        except OSError:
            utils.log_event('Error in delete temp dump file `%s` from `%s` db' % (exp_loc, self.__class__.__name__),
                            'warning', exc_info=True)

    def delete_zip_temp(self) -> None:
        """
        Deletes the temporary zip file.

        Logs a message indicating success or failure of the deletion.
        """
        exp_loc = self.get_exp_compress_file_location()
        try:
            utils.delete_item(exp_loc)
            utils.log_event(
                'Temp zip file `%s` from `%s` db deleted successfully!' % (exp_loc, self.__class__.__name__), 'debug')
        except OSError:
            utils.log_event('Error in delete temp zip file `%s` from `%s` db' % (exp_loc, self.__class__.__name__),
                            'warning', exc_info=True)

    @classmethod
    def check(cls, raise_exc: bool = True) -> bool:
        """
            Checks the database connection status.

            Args:
                raise_exc (bool): Whether to raise an exception on failure.

            Returns:
                bool: True if the connection is successful, False otherwise.

            Raises:
                Exception: If there is an issue with the database connection.
        """
        if cls._check_status:
            return cls._check_status
        if cls.IMPORT_STATUS is False:
            return False
        try:
            cls.connect()
            cls.close()
            cls._check_status = True
            return True
        except Exception as e:
            cls._check_status = False
            msg = 'There is some problem in checking %s db. more info [%s]' % (cls.__name__, e)
            utils.log_event(msg, 'error')
            if raise_exc:
                raise Exception(msg)
        return False

    def add_additional_args(self, args: list) -> None:
        """
            Adds additional arguments to the command.

            Args:
                args (list): A list of additional argument names to add to the command.
        """
        CMD = self.CMD or ''
        for arg in args:
            arg_cmd = self.ADDITIONAL_ARGS.get(arg)
            if not arg_cmd:
                utils.log_event('Additional arg `%s` not found' % arg, 'warning')
                continue
            CMD += f' {arg_cmd} '

        self.CMD = CMD

    def get_additional_args_name_as_list(self) -> list:
        """
            Gets additional argument names as a list of dictionaries.

            Returns:
                list: A list of dictionaries containing names and values of additional arguments.
        """
        args = self.ADDITIONAL_ARGS_NAME
        r = [{'name': an, 'value': av} for an, av in args.items()]
        return r

    def normalize_location(self, location: Union[str, Path]) -> Path:
        """
            Normalizes the location string by adding quotes.

            Args:
                location (Path): The location string to normalize.

            Returns:
                str: The normalized location string with quotes.
        """
        return Path('"{}"'.format(location))

    def _get_backup(self) -> Path:
        """
            Initiates the backup process.

            Returns:
                The result of the dump operation.
        """
        return self.dump()
