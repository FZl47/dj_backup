import pathlib
import logging
import zipfile
import os
import random
import string
import shutil
import platform

from django.utils import timezone
from dj_backup import settings

plt = platform.system()
_logger = logging.getLogger()


def random_str(n=7, characters=string.ascii_letters + string.digits):
    return ''.join(random.choice(characters) for _ in range(n))


def get_time(frmt='%Y-%m-%d'):
    return timezone.now().strftime(frmt)


def get_files_dir(*locations):
    return (pathlib.Path(loc).iterdir() for loc in locations)


def get_location(location):
    return pathlib.Path(location)


def is_dir(path):
    return os.path.isdir(path)


def is_subdirectory(root, sub):
    try:
        root = os.path.abspath(root)
        sub = os.path.abspath(sub)
        return os.path.commonpath([root]) == os.path.commonpath([root, sub])
    except:
        return False


def zip_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))


def zip_file(file_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(file_path, arcname=os.path.basename(file_path))


def zip_item(directory_or_file, zip_name):
    if is_dir(directory_or_file):
        zip_directory(directory_or_file, zip_name)
    else:
        zip_file(directory_or_file, zip_name)


def get_or_create_dir(item_path):
    p = pathlib.Path(item_path)
    return p.mkdir(exist_ok=True, parents=True)


def delete_item(item_path):
    if is_dir(item_path):
        shutil.rmtree(item_path)
    else:
        os.remove(item_path)


def copy_item(src, dest):
    if is_dir(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dest)


def get_file_name(path):
    return pathlib.Path(path).name


def get_file_size(path):
    return os.path.getsize(path)  # bytes


def file_is_exists(path):
    return os.path.exists(path)


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def join_paths(*paths):
    return os.path.join(*paths)


def get_os_name():
    return plt


def log_event(msg, level='info', exc_info=False, **kwargs):
    level = level.upper()
    levels = {
        'NOTSET': 0,
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50,
    }
    logging.log(levels[level], msg=msg, exc_info=exc_info, **kwargs)
