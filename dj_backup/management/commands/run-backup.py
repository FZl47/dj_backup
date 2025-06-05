from django.core.management.base import BaseCommand

from dj_backup import settings
from dj_backup.core import utils, storages


class Command(BaseCommand):
    help = 'Start and Run dj_backup'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('DJ-Backup STARTING...'))

        self.stdout.write(self.style.SUCCESS('CREATE BACKUP DIRS...'))
        # create dirs
        self.create_backup_dirs()

        # initial storages
        self.stdout.write(self.style.SUCCESS('INITIAL STORAGES...'))
        self.initial_storages()

        self.stdout.write(self.style.SUCCESS('TASK RUNNER STARTED ..!'))

        from dj_backup.core.task import runner
        runner.run()

    @staticmethod
    def initial_storages():
        # create storages object
        storages.initial_storages_obj()

    @staticmethod
    def create_backup_dirs():
        # create backup temp dir
        utils.get_or_create_dir(settings.get_backup_temp_dir())
        # create backup sys dir
        utils.get_or_create_dir(settings.get_backup_sys_dir())

        utils.log_event('Backup dirs were created successfully', 'debug')
