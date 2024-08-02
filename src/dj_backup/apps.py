from django.apps import AppConfig


class DjBackupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_backup'

    def ready(self):
        from .core import tasks