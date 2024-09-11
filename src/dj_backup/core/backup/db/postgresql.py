import os
import subprocess
import psycopg2
import pathlib

from django.utils.translation import gettext_lazy as _

from dj_backup.core import utils
from dj_backup import settings

from .base import BaseDB


class PostgresqlDB(BaseDB):
    CONFIG = {
        'NAME': None,
        'USER': None,
        'PASSWORD': None,
        'HOST': None,
        'PORT': 5432,
    }
    ADDITIONAL_ARGS_NAME = {
        'only_data': _('Only data'),
        'only_structure': _('Only structure'),
        'create_db': _('Create database'),
        'ignore_if_exists': _('Ignore if data(table,schema,object or ..) is exists'),
    }
    ADDITIONAL_ARGS = {
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
    def connect(cls):
        if cls._DB:
            return cls._DB
        c = cls.CONFIG
        try:
            db = psycopg2.connect(host=c['HOST'], port=int(c['PORT']), user=c['USER'],
                                  password=c['PASSWORD'], database=c['NAME'])
        except psycopg2.Error as e:
            msg = 'Postgresql connection error. please check your config or service status. more info [%s]' % e
            utils.log_event(msg, 'error', exc_info=True)
            raise psycopg2.Error(msg)
        cls._DB = db
        return cls._DB

    @classmethod
    def close(cls):
        if cls._DB:
            cls._DB.close()
            cls._DB = None

    def get_pg_dump_win(self):
        """
            get pg_dump location in windows
        """

        def get_postgresql_base_dir():
            if self._BASE_DIR:
                return self._BASE_DIR
            cmd = """
                SHOW data_directory;
            """
            db = self.connect()
            curs = db.cursor()
            try:
                curs.execute(cmd)
            except db.Error:
                msg = 'Variable `data_directory` not found in postgresql global variables'
                utils.log_event(msg, 'error', exc_info=True)
                raise
            base_dir = curs.fetchone()[0]
            curs.close()
            self.close()
            self._BASE_DIR = base_dir
            return self._BASE_DIR

        base_dir = pathlib.Path(get_postgresql_base_dir()).parent

        dump_path = utils.find_file(self.DUMP_PREFIX_WIN, base_dir)
        if not dump_path:
            msg = 'File `%s` not found in %s path' % (self.DUMP_PREFIX_WIN, base_dir)
            utils.log_event(msg, 'critical')
            raise FileNotFoundError(msg)
        return dump_path

    def get_dump_prefix(self):
        dump_path = settings.get_config().get('POSTGRESQL_DUMP_PATH', None)
        if dump_path:
            return self.normalize_location(dump_path)
        if utils.get_os_name() == 'Windows':
            return self.normalize_location(self.get_pg_dump_win())
        return self.normalize_location(self.DUMP_PREFIX)

    def prepare_cmd(self):
        """
            note: space in cmd string is important
        """
        c = self.CONFIG

        CMD = f" {self.get_dump_prefix()} -p {c['PORT']} -h {c['HOST']} -U {c['USER']} "

        # set password in environment
        password = c['PASSWORD']
        if password:
            os.putenv('PGPASSWORD', password)

        CMD += f" -d {c['NAME']} -f {self.normalized_export_location} "

        self.CMD = CMD

        # add additional args
        args = self.backup_obj.get_additional_args()
        self.add_additional_args(args)

    def dump(self):
        self.prepare_cmd()
        try:
            # execute command
            # TODO: add exception handler for shell errors
            subprocess.Popen(self.CMD, shell=True).wait()
        except subprocess.SubprocessError:
            msg = 'There is some problem in dump run command db: `%s` cmd: `%s`' % (self.CMD, self.__class__.__name__)
            utils.log_event(msg, 'critical')
            raise subprocess.SubprocessError(msg)
        # compress dump file
        exp_loc = self.export_location
        exc_loc_compress = self.get_exp_compress_file_location()
        try:
            utils.zip_file(exp_loc, exc_loc_compress)
        except (IOError, TypeError):
            msg = 'There is some problem in dump `%s` db' % self.__class__.__name__
            utils.log_event(msg, 'critical', exc_info=True)
        return exc_loc_compress


