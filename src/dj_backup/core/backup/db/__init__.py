"""
This module provides functionality to import and manage database connectors for different database engines.

It defines a mapping of supported database types to their respective modules and classes. The main functionalities include:

1. **Database Connector Importing**:
   - The `import_db_connector(db_type)` function imports the specified database connector based on the provided database type.
   - It handles exceptions for unknown database types and connectors, logging warnings accordingly.

2. **Database Availability Check**:
   - The `_get_databases_available()` function retrieves the database configurations from the settings and attempts to import the corresponding database connectors.
   - It sets the configuration for each database connector and checks their availability. If a connector is available, it is added to the `DATABASES_AVAILABLE` list.

Attributes:
- `ALL_DATABASES_DICT`: A dictionary storing the imported database classes by their types.
- `DATABASES_AVAILABLE`: A list that holds the available database connectors after checking their configurations.

Usage:
- Call `_get_databases_available()` to populate the `DATABASES_AVAILABLE` list with valid database connectors based on the project's settings.

Note:
- Ensure that the necessary database engine packages are installed and accessible in the environment for successful connector imports.
"""

import importlib

from typing import Union

from dj_backup.core.utils import log_event
from dj_backup import settings

_DATABASES_MODULE = {
    'sqlite3': ('dj_backup.core.backup.db.sqlite', 'SqliteDB'),
    'mysql': ('dj_backup.core.backup.db.mysql', 'MysqlDB'),
    'postgresql': ('dj_backup.core.backup.db.postgresql', 'PostgresqlDB'),
}

ALL_DATABASES_DICT = {}
DATABASES_AVAILABLE = []

for db_mod in _DATABASES_MODULE.keys():
    ALL_DATABASES_DICT[db_mod] = None


def import_db_connector(db_type: str) -> Union[object, None]:
    """
        Import database connector module
    """
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


def _get_databases_available() -> None:
    """
        Get databases from config and import then
    """
    databases_config = settings.get_databases_config()
    for db_config_name, db_config in databases_config.items():
        db_type = db_config['ENGINE']
        db_type = db_type.split('.')[-1]

        db_cls = import_db_connector(db_type)

        if not db_cls:
            continue

        ALL_DATABASES_DICT[db_type] = db_cls
        db_cls.set_config(db_config)
        db_cls.set_config_name(db_config_name)
        if db_cls.check():
            DATABASES_AVAILABLE.append(db_cls)


_get_databases_available()
