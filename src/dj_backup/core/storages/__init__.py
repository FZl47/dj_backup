from django.utils.translation import gettext_lazy as _

from dj_backup import settings, models

from .local import LocalStorageConnector
from .ftp_server import FTPServerConnector
from .sftp_server import SFTPServerConnector
from .drop_box import DropBoxConnector
from .telegram_bot import TelegramBOTConnector

ALL_STORAGES_DICT = {
    'LOCAL': LocalStorageConnector,
    'SFTP_SERVER': SFTPServerConnector,
    'FTP_SERVER': FTPServerConnector,
    'DROPBOX': DropBoxConnector,
    'TELEGRAM_BOT': TelegramBOTConnector,
}
STORAGES_AVAILABLE = []
STORAGES_CLASSES_CHECKED = []


def _check_storages_config():
    storages_config = settings.get_storages_config()
    for st_name, st_config in storages_config.items():
        try:
            storage_cls = ALL_STORAGES_DICT[st_name]
        except KeyError:
            raise ValueError('Unknown `%s` storage' % st_name)

        storage_cls.set_config(st_config)

        if storage_cls.check():
            STORAGES_CLASSES_CHECKED.append(storage_cls)


def _get_storage_config(storage_name):
    return settings.get_storages_config()[storage_name]


def _reset_storages_state():
    models.DJStorage.objects.filter(checked=True).update(checked=False)


_load_storages_initialized = False


def load_storage():
    # NOTE! load and call only with main runner
    global _load_storages_initialized
    if _load_storages_initialized:
        return
    storages_obj = models.DJStorage.objects.filter(checked=True)
    for storage_obj in storages_obj:
        storage_cls = storage_obj.storage_class
        storage_cls.set_config(_get_storage_config(storage_obj.name))
        STORAGES_AVAILABLE.append(storage_cls)

    _load_storages_initialized = True


def initial_storages_obj():
    """
        check and create storages object
        NOTE! call function only with run-command
    """

    _check_storages_config()
    _reset_storages_state()

    storages_obj_dict = [
        {'name': 'LOCAL', 'display_name': _('Local')},
        {'name': 'SFTP_SERVER', 'display_name': _('Sftp server')},
        {'name': 'FTP_SERVER', 'display_name': _('Ftp server')},
        {'name': 'DROPBOX', 'display_name': _('Dropbox')},
        {'name': 'TELEGRAM_BOT', 'display_name': _('Telegram Bot')},
    ]
    for storages_obj_dict in storages_obj_dict:
        storage_obj, created = models.DJStorage.objects.get_or_create(name=storages_obj_dict['name'],
                                                                      display_name=storages_obj_dict['display_name'],
                                                                      defaults={'name': storages_obj_dict['name']})
        if storage_obj.storage_class in STORAGES_CLASSES_CHECKED:
            storage_obj.checked = True
        else:
            storage_obj.checked = False
        storage_obj.save(update_fields=['checked'])
