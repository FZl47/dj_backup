import sqlite3

from dj_backup.core import utils

from .base import BaseDB


class SqliteDB(BaseDB):
    CONFIG = {
        'NAME': None,
    }
    NAME = 'sqlite'
    _DB = None

    @classmethod
    def connect(cls):
        if cls._DB:
            return cls._DB
        db_name = cls.CONFIG['NAME']
        try:
            # TODO: check exception handler
            # check db is exists
            if not utils.file_is_exists(db_name):
                raise sqlite3.DatabaseError('Database `%s` not exists' % db_name)
            db = sqlite3.connect(db_name).cursor()
        except sqlite3.DatabaseError as e:
            msg = 'sqlite connection error. please check your config or service status. more info [%s]' % e
            utils.log_event(msg, 'error', exc_info=True)
            raise sqlite3.DatabaseError(msg)
        cls._DB = db
        return cls._DB

    @classmethod
    def close(cls):
        if cls._DB:
            cls._DB.close()
            cls._DB = None

    def prepare_cmd(self):
        pass

    def dump(self):
        """
            get a copy of db file
        """
        name = self.CONFIG['NAME']
        exc_loc_compress = self.get_exp_compress_file_location()
        try:
            utils.zip_file(name, exc_loc_compress)
        except (IOError, TypeError):
            msg = 'There is some problem in dump `%s` db' % self.__class__.__name__
            utils.log_event(msg, 'critical', exc_info=True)
            raise
        return exc_loc_compress
