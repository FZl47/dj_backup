from django.utils.functional import SimpleLazyObject

from dj_backup.config import Settings


def load_settings():
    return Settings()


settings = SimpleLazyObject(load_settings)
