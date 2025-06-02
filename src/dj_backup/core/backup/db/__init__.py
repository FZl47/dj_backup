from dj_backup.core.backup.db import mysql, sqlite, postgresql
from dj_backup.core.backup.db import sqlite
from dj_backup import settings

ALL_DATABASES_DICT = {
    'sqlite': sqlite.SqliteDB,
    'sqlite3': sqlite.SqliteDB,
    'mysql': mysql.MysqlDB,
    'postgresql': postgresql.PostgresqlDB
}

DATABASES_AVAILABLE = []


def _get_databases_available():
    databases_config = settings.get_databases_config()
    for db_config_name, db_config in databases_config.items():
        db_type = db_config['ENGINE']
        db_type = db_type.split('.')[-1]
        try:
            db_cls = ALL_DATABASES_DICT[db_type]
        except KeyError:
            raise ValueError('Unknown `%s` database' % db_type)

        db_cls.set_config(db_config)
        db_cls.set_config_name(db_config_name)
        if db_cls.check():
            DATABASES_AVAILABLE.append(db_cls)


_get_databases_available()
