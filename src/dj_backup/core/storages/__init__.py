import importlib

from typing import Optional, Dict, Any

from django.utils.translation import gettext_lazy as _

from dj_backup import settings, models
from dj_backup.core.utils import log_event


_STORAGES_MODULE: Dict[str, tuple] = {
    'LOCAL': ('dj_backup.core.storages.local', 'LocalStorageConnector'),
    'SFTP_SERVER': ('dj_backup.core.storages.sftp_server', 'SFTPServerConnector'),
    'FTP_SERVER': ('dj_backup.core.storages.ftp_server', 'FTPServerConnector'),
    'DROPBOX': ('dj_backup.core.storages.drop_box', 'DropBoxConnector'),
    'TELEGRAM_BOT': ('dj_backup.core.storages.telegram_bot', 'TelegramBOTConnector'),
}

ALL_STORAGES_DICT: Optional[Dict[str, Any]] = None
STORAGES_AVAILABLE: list = []
STORAGES_AVAILABLE_DICT: Dict[str, Any] = {}
STORAGES_CLASSES_CHECKED: list = []


def import_storage_connector(storage_name: str) -> Optional[object]:
    """
        Import the storage connector class for the given storage name.

        :param storage_name: The name of the storage to import.
        :return: The storage connector class or None if an error occurs.
    """
    try:
        storage = _STORAGES_MODULE[storage_name]
        n_package, n_connector = storage
        storage_mod = importlib.import_module(n_package)
        storage_connector = getattr(storage_mod, n_connector)
        return storage_connector
    except KeyError:
        log_event(f"Unknown '{storage_name}' storage. Can't be imported.", 'warning', exc_info=True)
        return None
    except AttributeError:
        log_event(f"Unknown '{n_connector}' storage connector.", 'warning', exc_info=True)
        return None


def _check_storages_config() -> None:
    """
        Check and initialize storage configurations.

        This function sets up each storage connector based on the configuration settings.
    """
    storages_config = settings.get_storages_config()
    for st_name, st_config in storages_config.items():
        storage_connector = import_storage_connector(st_name)
        ALL_STORAGES_DICT[st_name] = storage_connector
        if not storage_connector:
            continue
        storage_connector.set_config(st_config)
        try:
            storage_connector.setup()
        except Exception as e:
            msg = f"There is some problem in setup storage `{storage_connector.STORAGE_NAME}` more detail [{e}]"
            log_event(msg, 'error', exc_info=True)
            raise Exception(msg)
        if storage_connector.check():
            STORAGES_CLASSES_CHECKED.append(storage_connector)
            STORAGES_AVAILABLE_DICT[st_name] = storage_connector
            STORAGES_AVAILABLE.append(storage_connector)


def _get_storage_config(storage_name: str) -> Optional[Dict[str, Any]]:
    """
        Retrieve the configuration for the specified storage.

        :param storage_name: The name of the storage.
        :return: The configuration dictionary or None if not found.
    """
    try:
        return settings.get_storages_config()[storage_name]
    except KeyError:
        log_event(f'Storage [{storage_name}] config is not available anymore', 'warning', exc_info=True)
        return None


def _reset_storages_state() -> None:
    """
        Reset the checked state of all storage objects in the database.
    """
    models.DJStorage.objects.filter(checked=True).update(checked=False)


_load_storages_initialized: bool = False


def load_storage() -> None:
    """
        Load storage connectors and initialize them.

        This function should be called only with the main runner.
    """
    global _load_storages_initialized
    if _load_storages_initialized:
        return

    storages_obj = models.DJStorage.objects.filter(checked=True)
    for storage_obj in storages_obj:
        storage_connector = import_storage_connector(storage_obj.name)
        if not storage_connector:
            log_event(f'There does not exist storage with `{storage_obj.name}` name', 'warning')
            continue
        storage_config = _get_storage_config(storage_obj.name)
        if not storage_config:
            continue
        storage_connector.set_config(storage_config)
        STORAGES_AVAILABLE_DICT[storage_obj.name] = storage_connector
        STORAGES_AVAILABLE.append(storage_connector)

    _load_storages_initialized = True


def initial_storages_obj() -> None:
    """
        Check and create storage objects.

        This function should be called only with run-command.
    """
    _check_storages_config()
    _reset_storages_state()

    storages_obj_dict = [
        {'name': 'LOCAL', 'display_name': _('Local')},
        {'name': 'SFTP_SERVER', 'display_name': _('SFTP Server')},
        {'name': 'FTP_SERVER', 'display_name': _('FTP Server')},
        {'name': 'DROPBOX', 'display_name': _('Dropbox')},
        {'name': 'TELEGRAM_BOT', 'display_name': _('Telegram Bot')},
    ]
    for storage_info in storages_obj_dict:
        storage_obj, created = models.DJStorage.objects.get_or_create(
            name=storage_info['name'],
            display_name=storage_info['display_name'],
            defaults={'name': storage_info['name']}
        )
        storage_obj.checked = storage_obj.storage_class in STORAGES_CLASSES_CHECKED
        storage_obj.save(update_fields=['checked'])
