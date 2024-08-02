from django.core.management.base import BaseCommand
from django.core.management import call_command

from dj_backup import settings


class Command(BaseCommand):
    help = 'Start and run DJ Backup'

    def handle(self, *args, **kwargs):
        # TODO: must be completed
        self.stdout.write(self.style.SUCCESS('DJ-Backup STARTING ...'))
        settings.create_backup_dirs()
        self.stdout.write(self.style.SUCCESS('CREATE BACKUP DIRS !'))
        self.stdout.write(self.style.SUCCESS('STARTED !'))

        # run django-q
        call_command('qcluster')
