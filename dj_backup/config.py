from django.conf import settings as django_settings


class Settings:
    listen_to_tasks_time_loop = 5  # seconds

    def __init__(self):
        self._check_config()

    @property
    def is_email_configured(self):
        if django_settings.EMAIL_HOST_USER and django_settings.EMAIL_HOST_PASSWORD:
            return True
        return False

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

    @classmethod
    def get_backup_sys_dir(cls):
        _default = django_settings.BASE_DIR / 'backup/sys'
        return django_settings.DJ_BACKUP_CONFIG.get('BACKUP_SYS_DIR', _default)

    @classmethod
    def get_max_workers_count(cls):
        return django_settings.DJ_BACKUP_CONFIG.get('MAX_WORKERS', 3)

    @classmethod
    def get_notification_object_log_level(cls):
        return django_settings.DJ_BACKUP_CONFIG.get('NOTIFICATION_OBJECT_LOG_LEVEL', 'WARNING').upper()

    @classmethod
    def get_log_level_num(cls):
        return {
            'NOTSET': 0,
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50,
        }
