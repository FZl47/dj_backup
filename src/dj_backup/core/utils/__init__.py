import pathlib
import zipfile
import os
import random
import string
import shutil
import platform

from typing import Union, Generator

from django.utils import timezone

# using by utils file
from dj_backup.core.logging import log_event

plt = platform.system()


def random_str(n=7, characters=string.ascii_letters + string.digits) -> str:
    """
        Generate a random string of specified length.

        Args:
            n (int): Length of the random string. Default is 7.
            characters (str): Characters to choose from. Default is alphanumeric.

        Returns:
            str: A random string of length `n`.
    """
    return ''.join(random.choice(characters) for _ in range(n))


def get_time(frmt='%Y-%m-%d') -> str:
    """
        Get the current time formatted as a string.

        Args:
            frmt (str): Format for the output time string. Default is '%Y-%m-%d'.

        Returns:
            str: The current time as a formatted string.
    """
    return timezone.now().strftime(frmt)


def get_files_dir(*locations) -> Generator:
    """
        Get an iterator of files in the specified directories.

        Args:
            locations (str): One or more directory paths.

        Returns:
            generator: An iterator of files in the specified directories.
    """
    return (pathlib.Path(loc).iterdir() for loc in locations)


def get_location(location: str) -> pathlib.Path:
    """
        Get a Path object for the specified location.

        Args:
            location (str): The location to convert.

        Returns:
            pathlib.Path: A Path object representing the location.
    """
    return pathlib.Path(location)


def is_dir(path: Union[pathlib.Path, str]) -> bool:
    """
        Check if the specified path is a directory.

        Args:
            path Union[pathlib.Path, str]: The path to check.

        Returns:
            bool: True if the path is a directory, False otherwise.
    """
    return os.path.isdir(path)


def is_subdirectory(root: Union[pathlib.Path, str], sub: Union[pathlib.Path, str]) -> bool:
    """
        Check if a path is a subdirectory of another path.

        Args:
            root Union[pathlib.Path, str]: The root directory path.
            sub Union[pathlib.Path, str]: The subdirectory path.

        Returns:
            bool: True if `sub` is a subdirectory of `root`, False otherwise.
    """
    try:
        root = os.path.abspath(root)
        sub = os.path.abspath(sub)
        return os.path.commonpath([root]) == os.path.commonpath([root, sub])
    except (FileNotFoundError, OSError, ValueError):
        return False


def zip_directory(directory: Union[pathlib.Path, str], zip_name: Union[pathlib.Path, str]) -> None:
    """
        Create a zip archive of the specified directory.

        Args:
            directory Union[pathlib.Path, str]: The directory to zip.
            zip_name Union[pathlib.Path, str]: The name of the output zip file.
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))


def zip_file(file_path: Union[pathlib.Path, str], zip_name: str) -> None:
    """
        Create a zip archive containing a single file.

        Args:
            file_path: Union[pathlib.Path, str]: The file to zip.
            zip_name (str): The name of the output zip file.
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=os.path.basename(file_path))


def zip_item(directory_or_file: Union[pathlib.Path, str], zip_name: str) -> None:
    """
        Zip a directory or a file.

        Args:
            directory_or_file: Union[pathlib.Path, str]: The directory or file to zip.
            zip_name (str): The name of the output zip file.
    """
    if is_dir(directory_or_file):
        zip_directory(directory_or_file, zip_name)
    else:
        zip_file(directory_or_file, zip_name)


def get_or_create_dir(item_path: Union[pathlib.Path, str]) -> None:
    """
        Create a directory if it does not exist.

        Args:
            item_path Union[pathlib.Path, str]: The path of the directory to create.
    """
    p = pathlib.Path(item_path)
    p.mkdir(exist_ok=True, parents=True)


def delete_item(item_path: Union[pathlib.Path, str]) -> None:
    """
        Delete a file or directory.

        Args:
            item_path Union[Path, str]: The path of the item to delete.
    """
    if is_dir(item_path):
        shutil.rmtree(item_path)
    else:
        os.remove(item_path)


def copy_item(src: Union[pathlib.Path, str], dest: Union[pathlib.Path, str]) -> None:
    """
        Copy a file or directory to a new location.

        Args:
            src Union[Path, str]: The source file or directory.
            dest Union[Path, str]: The destination path.
    """
    if is_dir(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dest)


def get_file_name(path: Union[pathlib.Path, str]) -> str:
    """
        Get the name of a file from its path.

        Args:
            path Union[Path, str]: The file path.

        Returns:
            str: The name of the file.
    """
    return pathlib.Path(path).name


def get_file_size(path: Union[pathlib.Path, str]) -> int:
    """
        Get the size of a file in bytes.

        Args:
             path Union[Path, str]: The file path.

        Returns:
            int: The size of the file in bytes.
    """
    return os.path.getsize(path)


def file_is_exists(path: Union[pathlib.Path, str]) -> bool:
    """
        Check if a file or directory exists.

        Args:
            path Union[Path, str]: The path to check.

        Returns:
            bool: True if the file or directory exists, False otherwise.
    """
    return os.path.exists(path)


def find_file(name: str, path: Union[pathlib.Path, str]) -> Union[str, None]:
    """
        Find a file by name within a directory.

        Args:
            name (str): The name of the file to find.
            path (str): The directory path to search in.

        Returns:
            Union[Path, None]: The full path of the found file, or None if not found.
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def join_paths(*paths: str) -> str:
    """
        Join multiple paths into a single path.

        Args:
            *paths (str): Paths to join.

        Returns:
            str: The joined path.
    """
    return os.path.join(*paths)


def get_os_name() -> str:
    """
        Get the name of the operating system.

        Returns:
            str: The name of the operating system.
    """
    return plt
