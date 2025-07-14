import os
import subprocess
import warnings

from typing import Optional, Dict, Any

from pathlib import Path

try:
    import psycopg2

    package_imported = True
except ImportError:
    package_imported = False
    warnings.warn("""
        To back up database 'Postgresql', you need to install its package using the following command; otherwise, it cannot be used:
        'pip install djbackup[postgresql]'""")

from django.utils.translation import gettext_lazy as _

from dj_backup.core import utils
from dj_backup import settings

from .base import BaseDB


class PostgresqlDB(BaseDB):
    """
        A class to represent a PostgreSQL database connection and perform backup operations.

        Attributes:
            IMPORT_STATUS (bool): Indicates whether the psycopg2 package is imported successfully.
            CONFIG (dict): Configuration settings for connecting to the PostgreSQL database.
            ADDITIONAL_ARGS_NAME (dict): Descriptive names for additional arguments used in dump operations.
            ADDITIONAL_ARGS (dict): Command-line arguments for pg_dump operations.
            NAME (str): Name of the database type.
            DUMP_PREFIX (str): Command prefix for pg_dump in Unix-like systems.
            DUMP_PREFIX_WIN (str): Command prefix for pg_dump in Windows.
            _BASE_DIR (Optional[str]): Base directory of the PostgreSQL installation.
            _DB (Optional[psycopg2.extensions.connection]): Connection object for the PostgreSQL database.
    """

    IMPORT_STATUS = package_imported
    CONFIG: Dict[str, Optional[Any]] = {
        'NAME': None,
        'USER': None,
        'PASSWORD': None,
        'HOST': None,
        'PORT': 5432,
    }
    ADDITIONAL_ARGS_NAME: Dict[str, Optional[Any]] = {
        'only_data': _('Only data'),
        'only_structure': _('Only structure'),
        'create_db': _('Create database'),
        'ignore_if_exists': _('Ignore if data (table, schema, object, etc.) exists'),
    }
    ADDITIONAL_ARGS: Dict[str, Optional[Any]] = {
        'only_data': '--data-only',
        'only_structure': '--schema-only',
        'create_db': '--create',
        'ignore_if_exists': '--if-exists',
    }
    NAME = 'postgresql'
    DUMP_PREFIX = 'pg_dump'
    DUMP_PREFIX_WIN = 'pg_dump.exe'
    _BASE_DIR = None
    _DB = None

    @classmethod
    def connect(cls) -> psycopg2.extensions.connection:
        """
            Connect to the PostgreSQL database and return the connection object.
    
            Raises:
                psycopg2.Error: If there is an error connecting to the database.
        """
        if cls._DB:
            return cls._DB
        c = cls.CONFIG
        try:
            db = psycopg2.connect(host=c['HOST'], port=int(c['PORT']), user=c['USER'],
                                  password=c['PASSWORD'], database=c['NAME'])
        except psycopg2.Error as e:
            msg = 'Postgresql connection error. Please check your config or service status. More info [%s]' % e
            utils.log_event(msg, 'error', exc_info=True)
            raise psycopg2.Error(msg)
        cls._DB = db
        return cls._DB

    @classmethod
    def close(cls) -> None:
        """
            Close the PostgreSQL database connection.
        """
        if cls._DB:
            cls._DB.close()
            cls._DB = None

    def get_pg_dump_win(self) -> str:
        """
            Get the pg_dump location in Windows.
    
            Returns:
                str: The path to pg_dump.
    
            Raises:
                FileNotFoundError: If the pg_dump file is not found.
        """

        def get_postgresql_base_dir() -> str:
            """
                Retrieve the PostgreSQL base directory.
    
                Returns:
                    str: The base directory of PostgreSQL.
    
                Raises:
                    Exception: If the data_directory variable is not found.
            """
            if self._BASE_DIR:
                return self._BASE_DIR
            cmd = "SHOW data_directory;"
            db = self.connect()
            curs = db.cursor()
            try:
                curs.execute(cmd)
            except db.Error:
                msg = 'Variable `data_directory` not found in PostgreSQL global variables'
                utils.log_event(msg, 'error', exc_info=True)
                raise
            base_dir = curs.fetchone()[0]
            curs.close()
            self.close()
            self._BASE_DIR = base_dir
            return self._BASE_DIR

        base_dir = Path(get_postgresql_base_dir()).parent
        dump_path = utils.find_file(self.DUMP_PREFIX_WIN, base_dir)
        if not dump_path:
            msg = 'File `%s` not found in %s path' % (self.DUMP_PREFIX_WIN, base_dir)
            utils.log_event(msg, 'critical')
            raise FileNotFoundError(msg)
        return dump_path

    def get_dump_prefix(self) -> Path:
        """
            Get the dump prefix based on the configuration or OS.
    
            Returns:
                Path: The dump prefix path.
        """
        dump_path = settings.get_config().get('POSTGRESQL_DUMP_PATH', None)
        if dump_path:
            return self.normalize_location(dump_path)
        if utils.get_os_name() == 'Windows':
            return self.normalize_location(self.get_pg_dump_win())
        return self.normalize_location(self.DUMP_PREFIX)

    def prepare_cmd(self) -> None:
        """
            Prepare the command for dumping the database.
    
            Note: Space in cmd string is important.
        """
        c = self.CONFIG
        CMD = f"{self.get_dump_prefix()} -p {c['PORT']} -h {c['HOST']} -U {c['USER']} "

        # Set password in environment
        password = c['PASSWORD']
        if password:
            os.putenv('PGPASSWORD', password)

        CMD += f" -d {c['NAME']} -f {self.normalized_export_location} "
        self.CMD = CMD

        # Add additional args
        args = self.backup_obj.get_additional_args()
        self.add_additional_args(args)

    def dump(self) -> Path:
        """
            Execute the dump command and compress the dump file.
    
            Returns:
                Path: The location of the compressed dump file.
    
            Raises:
                subprocess.SubprocessError: If there is an error executing the dump command.
        """
        self.prepare_cmd()
        try:
            # Execute command
            subprocess.Popen(self.CMD, shell=True).wait()
        except subprocess.SubprocessError:
            msg = 'There is some problem in dump run command db: `%s` cmd: `%s`' % (self.CMD, self.__class__.__name__)
            utils.log_event(msg, 'critical')
            raise subprocess.SubprocessError(msg)

        # Compress dump file
        exp_loc = self.export_location
        exc_loc_compress = self.get_exp_compress_file_location()
        try:
            utils.zip_file(exp_loc, exc_loc_compress)
        except (IOError, TypeError):
            msg = 'There is some problem in dump `%s` db' % self.__class__.__name__
            utils.log_event(msg, 'critical', exc_info=True)
        return exc_loc_compress
