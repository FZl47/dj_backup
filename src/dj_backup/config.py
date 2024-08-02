from django.conf import settings as django_settings

from dj_backup.core import utils


class Settings:

    def __init__(self):
        self._check_config()

    @classmethod
    def _check_config(cls):
        # check config(in django settings)
        dj_config = cls._get_config()
        storages = dj_config.get('STORAGES')
        assert storages, 'You must define `STORAGES` in `DJ_BACKUP_CONFIG`'

    @classmethod
    def _get_config(cls):
        try:
            return django_settings.DJ_BACKUP_CONFIG
        except (AttributeError,):
            raise AttributeError('You must define `DJ_BACKUP_CONFIG` variable in settings')

    @classmethod
    def get_storages_config(cls):
        dj_config = cls._get_config()
        return dj_config.get('STORAGES')

    @classmethod
    def get_base_root(cls):
        _default = django_settings.BASE_DIR
        return django_settings.DJ_BACKUP_CONFIG.get('BASE_ROOT', _default)

    @classmethod
    def get_backup_dirs(cls):
        return django_settings.DJ_BACKUP_CONFIG['BACKUP_DIRS']

    @classmethod
    def get_backup_temp_dir(cls):
        _default = django_settings.BASE_DIR / 'backup/temp'
        return django_settings.DJ_BACKUP_CONFIG.get('BACKUP_TEMP_DIR', _default)

    @classmethod
    def create_backup_dirs(cls):
        # TODO: add log
        # TODO: better run in start command
        # create backup temp dir
        utils.get_or_create_dir(cls.get_backup_temp_dir())
        # create backup root dirs
        for d in cls.get_backup_dirs():
            utils.get_or_create_dir(d)
