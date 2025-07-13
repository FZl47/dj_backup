import importlib

from django.utils.translation import gettext_lazy as _

from dj_backup import settings, models
from dj_backup.core.utils import log_event

_STORAGES_MODULE = {
    'LOCAL': ('dj_backup.core.storages.local', 'LocalStorageConnector'),
    'SFTP_SERVER': ('dj_backup.core.storages.sftp_server', 'SFTPServerConnector'),
    'FTP_SERVER': ('dj_backup.core.storages.ftp_server', 'FTPServerConnector'),
    'DROPBOX': ('dj_backup.core.storages.drop_box', 'DropBoxConnector'),
    'TELEGRAM_BOT': ('dj_backup.core.storages.telegram_bot', 'TelegramBOTConnector'),
}

ALL_STORAGES_DICT = {}
STORAGES_AVAILABLE = []
STORAGES_AVAILABLE_DICT = {}
STORAGES_CLASSES_CHECKED = []

for st in _STORAGES_MODULE.keys():
    ALL_STORAGES_DICT[st] = None


def import_storage_connector(storage_name):
    try:
        storage = _STORAGES_MODULE[storage_name]
        n_package = storage[0]
        n_connector = storage[1]
        storage_mod = importlib.import_module(n_package)
        storage_connector = getattr(storage_mod, n_connector)
        return storage_connector
    except KeyError:
        log_event("Unknown '%s' storage. cant be import" % storage_name, 'warning', exc_info=True)
        return None
    except AttributeError:
        log_event("Unknown '%s' storage connector" % n_connector, 'warning', exc_info=True)
        return None


def _check_storages_config():
    storages_config = settings.get_storages_config()
    for st_name, st_config in storages_config.items():
        storage_connector = import_storage_connector(st_name)
        ALL_STORAGES_DICT[st_name] = storage_connector
        storage_connector.set_config(st_config)
        try:
            storage_connector.setup()
        except Exception as e:
            msg = "There is some problem in setup storage `%s` more detail [%s]" % (storage_connector.STORAGE_NAME, e)
            log_event(msg, 'error',
                      exc_info=True)
            raise Exception(msg)
        if storage_connector.check():
            STORAGES_CLASSES_CHECKED.append(storage_connector)
            STORAGES_AVAILABLE_DICT[st_name] = storage_connector
            STORAGES_AVAILABLE.append(storage_connector)


def _get_storage_config(storage_name):
    try:
        return settings.get_storages_config()[storage_name]
    except KeyError:
        log_event('Storage [%s] config is not available any more' % storage_name, 'warning', exc_info=True)
        return None


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
        storage_connector = import_storage_connector(storage_obj.name)
        if not storage_connector:
            log_event('There is not exists storage with `%s` name' % storage_obj.name, 'warning')
            continue
        storage_config = _get_storage_config(storage_obj.name)
        if not storage_config:
            continue
        storage_connector.set_config(storage_config)
        STORAGES_AVAILABLE_DICT[storage_obj.name] = storage_connector
        STORAGES_AVAILABLE.append(storage_connector)

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
