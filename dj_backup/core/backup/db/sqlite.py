import sqlite3

from typing import Optional, Dict, Any

from pathlib import Path

from dj_backup.core import utils

from .base import BaseDB


class SqliteDB(BaseDB):
    """
        A class to represent a SQLite database connection and perform backup operations.

        Attributes:
            CONFIG (dict): Configuration settings for connecting to the SQLite database.
            NAME (str): Name of the database type.
            _DB (Optional[sqlite3.Cursor]): Cursor object for the SQLite database.
    """

    CONFIG: Dict[str, Optional[Any]] = {
        'NAME': None,
    }
    NAME = 'sqlite3'
    _DB = None

    @classmethod
    def connect(cls) -> sqlite3.Cursor:
        """
            Connect to the SQLite database and return the cursor object.

            Returns:
                sqlite3.Cursor: The cursor object for the connected database.

            Raises:
                sqlite3.DatabaseError: If there is an error connecting to the database.
        """
        if cls._DB:
            return cls._DB
        db_name = cls.CONFIG['NAME']
        try:
            # Check if the database exists
            if not utils.file_is_exists(db_name):
                raise sqlite3.DatabaseError('Database `%s` does not exist' % db_name)
            db = sqlite3.connect(db_name).cursor()
        except sqlite3.DatabaseError as e:
            msg = 'SQLite connection error. Please check your config or service status. More info [%s]' % e
            utils.log_event(msg, 'error', exc_info=True)
            raise sqlite3.DatabaseError(msg)
        cls._DB = db
        return cls._DB

    @classmethod
    def close(cls) -> None:
        """
            Close the SQLite database connection.
        """
        if cls._DB:
            cls._DB.connection.close()
            cls._DB = None

    def prepare_cmd(self) -> None:
        """
            Prepare the command for dumping the database.
            `In This Case Not happening`
        """
        pass

    def delete_dump_file(self) -> None:
        """
            Delete the dump file if it exists.
            `In This Case Not happening`
        """
        pass

    def dump(self) -> Path:
        """
            Create a compressed copy of the SQLite database file.

            Returns:
                str: The location of the compressed dump file.

            Raises:
                IOError: If there is an error during the dump process.
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
