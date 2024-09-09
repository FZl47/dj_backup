import abc

from dj_backup.core import utils
from dj_backup import settings
from dj_backup.core.backup.base import BaseBackup


class BaseDB(BaseBackup):
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
        super().__init__()
        """
            backup_obj can be None. to prevent errors during usage in the template.
        """
        self.backup_obj = backup_obj
        if backup_obj:
            self.export_location = self._get_export_location()
            self.normalized_export_location = self.normalize_location(self.export_location)

    def _get_export_location(self):
        temp_dir = settings.get_backup_temp_dir()
        return utils.join_paths(temp_dir, self.backup_obj.get_backup_location(self.OUTPUT_FORMAT))

    def get_exp_compress_file_location(self):
        return f'{self.export_location}.zip'

    @classmethod
    def set_config(cls, config):
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
    def set_config_name(cls, name):
        cls.CONFIG_NAME = name

    @classmethod
    @abc.abstractmethod
    def connect(cls):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def close(cls):
        raise NotImplementedError

    @abc.abstractmethod
    def prepare_cmd(self):
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self):
        raise NotImplementedError

    def delete_dump_file(self):
        exp_loc = self.export_location

        try:
            utils.delete_item(exp_loc)
            utils.log_event(
                'Temp dump file `%s` from `%s` db deleted successfully!' % (exp_loc, self.__class__.__name__), 'debug')
        except OSError:
            utils.log_event('Error in delete temp dump file `%s` from `%s` db' % (exp_loc, self.__class__.__name__),
                            'warning', exc_info=True)

    @classmethod
    def check(cls, raise_exc=True):
        if cls._check_status:
            return cls._check_status
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

    def add_additional_args(self, args):
        CMD = self.CMD or ''
        for arg in args:
            arg_cmd = self.ADDITIONAL_ARGS.get(arg)
            if not arg_cmd:
                utils.log_event('Additional arg `%s` not found' % arg, 'warning')
                continue
            CMD += f' {arg_cmd} '

        self.CMD = CMD

    def get_additional_args_name_as_list(self):
        args = self.ADDITIONAL_ARGS_NAME
        r = [{'name': an, 'value': av} for an, av in args.items()]
        return r

    def normalize_location(self, location):
        # add dump location(To avoid errors, i put paths with spaces
        # inside double quotes.)
        return '"{}"'.format(location)
