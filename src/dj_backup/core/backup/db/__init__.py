import importlib

from dj_backup.core.utils import log_event
from dj_backup import settings

_DATABASES_MODULE = {
    'sqlite': ('dj_backup.core.backup.db.sqlite', 'SqliteDB'),
    'sqlite3': ('dj_backup.core.backup.db.sqlite', 'SqliteDB'),
    'mysql': ('dj_backup.core.backup.db.mysql', 'MysqlDB'),
    'postgresql': ('dj_backup.core.backup.db.postgresql', 'PostgresqlDB'),
}

ALL_DATABASES_DICT = {}
DATABASES_AVAILABLE = []

for db_mod in _DATABASES_MODULE.keys():
    ALL_DATABASES_DICT[db_mod] = None


def import_db_connector(db_type):
    try:
        db = _DATABASES_MODULE[db_type]
        n_package = db[0]
        n_connector = db[1]
        db_mod = importlib.import_module(n_package)
        db_connector = getattr(db_mod, n_connector)
        return db_connector
    except KeyError:
        log_event("Unknown '%s' database. cant be import" % db_type, 'warning', exc_info=True)
        return None
    except AttributeError:
        log_event("Unknown '%s' database connector" % n_connector, 'warning', exc_info=True)
        return None


def _get_databases_available():
    databases_config = settings.get_databases_config()
    for db_config_name, db_config in databases_config.items():
        db_type = db_config['ENGINE']
        db_type = db_type.split('.')[-1]

        db_cls = import_db_connector(db_type)
        ALL_DATABASES_DICT[db_type] = db_cls

        db_cls.set_config(db_config)
        db_cls.set_config_name(db_config_name)
        if db_cls.check():
            DATABASES_AVAILABLE.append(db_cls)


_get_databases_available()
