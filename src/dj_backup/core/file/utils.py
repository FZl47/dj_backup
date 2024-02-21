import pathlib
import zipfile
import os
import shutil
from django.conf import settings


def get_files_dir(root_location=None):
    root_location = root_location or settings.DJ_BACKUP_CONFIG['BASE_ROOT']
    files = pathlib.Path(root_location).iterdir()
    return files


def get_location(location):
    return pathlib.Path(location)


def zip_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))


def zip_file(file_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(file_path, arcname=file_path)


def zip_item(directory_or_file, zip_name):
    if os.path.isdir(directory_or_file):
        zip_directory(directory_or_file, zip_name)
    else:
        zip_file(directory_or_file, zip_name)


def get_or_create_dir(item_path):
    p = pathlib.Path(item_path)
    return p.mkdir(exist_ok=True)


def delete_file(item_path):
    try:
        os.remove(item_path)
    except OSError:
        # File does not exist
        # TODO: log err
        pass


def copy_item(src, dest):
    try:
        shutil.copy2(src, dest)
    except IOError as e:
        # TODO: log err
        pass
