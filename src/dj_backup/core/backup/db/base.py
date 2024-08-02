import subprocess
from django.conf import settings

DJ_BACKUP_CONFIG = settings.DJ_BACKUP_CONFIG
DATABASES = settings.DATABASES


class BaseDB:
    temp_dir = DJ_BACKUP_CONFIG['BACKUP_TEMP_DIR']

    def get_export_location(self):
        return self.temp_dir.joinpath(f'{self.NAME}-exports-test.sql')


class MysqlDB(BaseDB):
    NAME = 'mysql'
    CMD = ''
    dump_prefix = 'mysqldump'

    def __init__(self):
        db_config = DATABASES['default']  # TODO add multiple database in future
        self.db_name = db_config['NAME']
        self.db_user = db_config['USER']
        self.db_pass = db_config['PASSWORD']
        self.db_host = db_config['HOST']
        self.db_port = db_config['PORT']

    def add_args(self):
        # TODO: add mysqldump location in window os (C:\\Users\\Test\\C:\\bin\\mysqldump or ..)
        self.CMD = '{dump_prefix} -P {port} -h {host} -u {user} -p{password} --databases {db_name} > {export_name}'.format(
            dump_prefix=self.dump_prefix, port=self.db_port, host=self.db_host, user=self.db_user,
            password=self.db_pass, db_name=self.db_name,
            export_name=self.get_export_location()
        )

    def dump(self):
        self.add_args()
        subprocess.Popen(self.CMD, shell=True)  # TODO: add log(stderr,stdout)
