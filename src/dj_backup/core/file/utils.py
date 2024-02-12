import pathlib
from django.conf import settings


def get_files_dir(root_location=None):
    root_location = root_location or settings.DJ_BACKUP_CONFIG['BASE_ROOT']
    files = pathlib.Path(root_location).iterdir()
    return files
