import subprocess
import warnings

try:
    import MySQLdb as _MySQLdb

    package_imported = True
except ImportError:
    package_imported = False
    warnings.warn("""
        To back up database 'Mysql', you need to install its package using the following command; otherwise, it cannot be used:
        'pip install djbackup[mysql]'""")

from django.utils.translation import gettext_lazy as _

from dj_backup.core import utils
from dj_backup import settings

from .base import BaseDB


class MysqlDB(BaseDB):
    IMPORT_STATUS = package_imported
    CONFIG = {
        'NAME': None,
        'USER': None,
        'PASSWORD': None,
        'HOST': None,
        'PORT': 3306,
    }
    ADDITIONAL_ARGS_NAME = {
        'only_data': _('Only data'),
        'only_structure': _('Only structure'),
        'no_db': _('No database creation'),
    }
    ADDITIONAL_ARGS = {
        'only_data': '--no-create-info',
        'only_structure': '--no-data',
        'no_db': '--no-create-db',
    }
    NAME = 'mysql'
    DUMP_PREFIX = 'mysqldump'
    DUMP_PREFIX_WIN = 'mysqldump.exe'
    _BASE_DIR = None
    _DB = None

    @classmethod
    def connect(cls):
        if cls._DB:
            return cls._DB
        c = cls.CONFIG
        try:
            db = _MySQLdb.connect(host=c['HOST'], port=int(c['PORT']), user=c['USER'],
                                  password=c['PASSWORD'], db=c['NAME'])
        except _MySQLdb.Error as e:
            msg = 'Mysql connection error. please check your config or service status. more info [%s]' % e
            utils.log_event(msg, 'error', exc_info=True)
            raise _MySQLdb.Error(msg)
        cls._DB = db
        return cls._DB

    @classmethod
    def close(cls):
        if cls._DB:
            cls._DB.close()
            cls._DB = None

    def get_mysqldump_win(self):
        """
            get mysqldump location in windows
        """

        def get_mysql_base_dir():
            if self._BASE_DIR:
                return self._BASE_DIR
            cmd = """
                SELECT @@GLOBAL.basedir;
            """
            db = self.connect()
            curs = db.cursor()
            try:
                curs.execute(cmd)
            except db.Error:
                msg = 'Variable `basedir` not found in mysql global variables'
                utils.log_event(msg, 'error', exc_info=True)
                raise
            base_dir = curs.fetchone()[0]
            curs.close()
            self.close()
            self._BASE_DIR = base_dir
            return self._BASE_DIR

        base_dir = get_mysql_base_dir()
        dump_path = utils.find_file(self.DUMP_PREFIX_WIN, base_dir)
        if not dump_path:
            msg = 'File `%s` not found in %s path' % (self.DUMP_PREFIX_WIN, base_dir)
            utils.log_event(msg, 'critical')
            raise FileNotFoundError(msg)
        return dump_path

    def get_dump_prefix(self):
        dump_path = settings.get_config().get('MYSQL_DUMP_PATH', None)
        if dump_path:
            return self.normalize_location(dump_path)
        if utils.get_os_name() == 'Windows':
            return self.normalize_location(self.get_mysqldump_win())
        return self.normalize_location(self.DUMP_PREFIX)

    def prepare_cmd(self):
        """
            note: space in cmd string is important
        """
        c = self.CONFIG

        CMD = f"{self.get_dump_prefix()} -P {c['PORT']} -h {c['HOST']} -u {c['USER']} "

        password = c['PASSWORD']
        if password:
            CMD += f" -p{password} "

        CMD += f" --databases {c['NAME']} --result-file={self.normalized_export_location} "

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
