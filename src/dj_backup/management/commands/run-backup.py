from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _

from dj_backup import settings
from dj_backup import models
from dj_backup.core import utils


class Command(BaseCommand):
    help = 'Start and run DJ Backup'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('DJ-Backup STARTING...'))

        self.stdout.write(self.style.SUCCESS('CREATE BACKUP DIRS...'))
        # create dirs
        self.create_backup_dirs()

        # initial storages
        self.stdout.write(self.style.SUCCESS('INITIAL STORAGES...'))
        self.initial_storages()

        self.stdout.write(self.style.SUCCESS('STARTED !'))

        # run django-q
        call_command('qcluster')

    @staticmethod
    def initial_storages():
        # create storages object
        models.DJStorage.objects.get_or_create(name='LOCAL', display_name=_('Local'),
                                               defaults={'name': 'LOCAL'})
        models.DJStorage.objects.get_or_create(name='SFTP_SERVER', display_name=_('Sftp server'),
                                               defaults={'name': 'SFTP_SERVER'})
        models.DJStorage.objects.get_or_create(name='FTP_SERVER', display_name=_('Ftp server'),
                                               defaults={'name': 'FTP_SERVER'})
        models.DJStorage.objects.get_or_create(name='DROPBOX', display_name=_('Dropbox'),
                                               defaults={'name': 'DROPBOX'})

    @staticmethod
    def create_backup_dirs():
        # create backup temp dir
        utils.get_or_create_dir(settings.get_backup_temp_dir())
        utils.log_event('Backup dirs were created successfully', 'debug')

