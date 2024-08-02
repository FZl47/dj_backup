from django.utils.translation import gettext_lazy as _
from django.db import models

from dj_backup.core import utils


class DJBackUpBase(models.Model):
    UNITS = (
        ('minutes', _('Minutes')),
        ('hours', _('Hours')),
        ('days', _('Days')),
        ('weeks', _('Weeks')),
    )

    name = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)

    unit = models.CharField(max_length=10, choices=UNITS)
    interval = models.SmallIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def convert_unit_interval_to_minute(self):
        u = self.unit
        if u == 'minutes':
            return self.interval
        elif u == 'hours':
            return self.interval * 60
        elif u == 'days':
            return self.interval * 24 * 60
        elif u == 'weeks':
            return self.interval * 7 * 24 * 60
        raise ValueError('you must set valid `unit` field')


class DJFileBackUp(DJBackUpBase):

    def get_files(self):
        return self.djfile_set.all()


class DJDatabaseBackUp(DJBackUpBase):
    pass


class DJFile(models.Model):
    name = models.CharField(max_length=200)
    backup = models.ForeignKey('DJFileBackUp', on_delete=models.CASCADE)
    dir = models.TextField()

    def save_temp_compress(self, base_dir_name):
        dest = f'{base_dir_name}/file__{self.name}.zip'
        utils.zip_item(self.dir, dest)
