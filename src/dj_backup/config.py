from django.conf import settings as django_settings


class Settings:

    def __init__(self):
        self._check_config()

    @classmethod
    def _check_config(cls):
        # check config(in django settings)
        dj_config = cls.get_config()
        storages = dj_config.get('STORAGES')
        assert storages, 'You must define `STORAGES` in `DJ_BACKUP_CONFIG`'

    @classmethod
    def get_config(cls):
        try:
            return django_settings.DJ_BACKUP_CONFIG
        except (AttributeError,):
            raise AttributeError('You must define `DJ_BACKUP_CONFIG` variable in settings')

    @classmethod
    def get_databases_config(cls):
        databases_dict = django_settings.DATABASES.copy()
        external_databases_dict = cls.get_config().get('EXTERNAL_DATABASES', {})
        databases_dict.update(external_databases_dict)
        return databases_dict

    @classmethod
    def get_storages_config(cls):
        dj_config = cls.get_config()
        return dj_config.get('STORAGES')

    @classmethod
    def get_base_root_dirs(cls):
        _default = django_settings.BASE_DIR
        return django_settings.DJ_BACKUP_CONFIG.get('BASE_ROOT_DIRS', [_default])

    @classmethod
    def get_backup_dirs(cls):
        return django_settings.DJ_BACKUP_CONFIG['BACKUP_DIRS']

    @classmethod
    def get_backup_temp_dir(cls):
        _default = django_settings.BASE_DIR / 'backup/temp'
        return django_settings.DJ_BACKUP_CONFIG.get('BACKUP_TEMP_DIR', _default)
