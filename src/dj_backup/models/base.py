import abc

from model_utils.managers import InheritanceManager

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db import models

from dj_backup.core import utils
from dj_backup.core import storages, backup


class DJBackupSecure(models.Model):
    ENCRYPTION_TYPES = (
        ('zipp', _('Zip Password')),
        ('aes', _('Advanced Encryption Standard')),
    )

    encryption_type = models.CharField(max_length=6, choices=ENCRYPTION_TYPES)
    key = models.CharField(max_length=256)
    backup = models.OneToOneField('DJBackUpBase', on_delete=models.CASCADE)


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
    schedule_task = models.OneToOneField('TaskSchedule', on_delete=models.SET_NULL, null=True, blank=True)
    last_run = models.DateTimeField(auto_now=True)
    repeats = models.SmallIntegerField(default=0)
    count_run = models.PositiveIntegerField(default=0)
    has_temp = models.BooleanField(default=True)
    has_running_task = models.BooleanField(default=False)
    storages = models.ManyToManyField('DJStorage', blank=True)
    results = models.ManyToManyField('DJBackUpStorageResult', blank=True)

    class Meta:
        ordering = ('-id',)

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    @property
    def unit_label(self):
        return self.get_unit_display()

    @property
    def is_running(self):
        if self.schedule_task:
            return True
        return False

    @property
    def has_storage(self):
        return self.get_storages().exists()

    @property
    def has_secure(self):
        return bool(self.get_secure())

    def get_secure(self):
        try:
            return self.djbackupsecure
        except AttributeError:
            return None

    @abc.abstractmethod
    def get_backup_location(self, *args, **kwargs):
        raise NotImplementedError

    def delete_temp_files(self):
        for r in self.get_results():
            r.delete_temp_file()

    def get_usage_size(self):
        return self.get_success_results().aggregate(total=models.Sum('size'))['total'] or 0

    def get_usage_size_by_storage(self, storage):
        return self.get_success_results().filter(storage=storage).aggregate(total=models.Sum('size'))['total'] or 0

    def get_count_backup_storage(self, storage):
        return self.results.filter(storage=storage).aggregate(total=models.Count('id'))['total'] or 0

    def get_last_run(self):
        return self.last_run.strftime('%Y-%d-%m %H:%M')

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

    def convert_unit_interval_to_seconds(self):
        return self.convert_unit_interval_to_minute() * 60

    def get_storages(self):
        return self.storages.all()

    def get_results(self):
        return self.results.all()

    def get_success_results(self):
        return self.get_results().filter(status='successful')

    def get_unsuccessful_results(self):
        return self.get_results().filter(status='unsuccessful')

    def get_absolute_url(self):
        return reverse_lazy('dj_backup:backup__detail', args=(self.id,))

    def delete_tasks(self):
        schedule_task = self.schedule_task
        if schedule_task:
            try:
                TaskSchedule.objects.get(task_id=self.schedule_task.task_id).delete()
            except TaskSchedule.DoesNotExist:
                utils.log_event('Task not found id: `%s`' % schedule_task.task_id, 'warning')

    def get_task_id(self):
        return 'schedule_backup_task_{}_{}'.format(self.name, self.id)


class DJFileBackUp(DJBackUpBase):
    backup_type = 'file'
    files = models.ManyToManyField('DJFile')

    def get_files(self):
        return self.files.all()

    def get_backup_location(self):
        t = utils.get_time('%Y-%m-%d_%H-%M')
        cr = self.count_run
        name = self.name.replace(' ', '-')
        return f'fb__{t}__{name}__{self.id}-{cr}'


class DJDataBaseBackUp(DJBackUpBase):
    backup_type = 'database'
    database = models.CharField(max_length=40)
    database_type = models.CharField(max_length=40)
    additional_args = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.database}'

    @property
    def db_ins(self):
        """
            get an instance of backup database classes
        """
        db_cls = self.get_db_cls()
        if not db_cls:
            return None
        return db_cls(self)

    def get_db_cls(self):
        """
            get backup database class
        """
        db_cls = backup.db.ALL_DATABASES_DICT.get(self.database_type)
        if not db_cls:
            msg = 'There is not exists database backup with `%s` name' % self.name
            utils.log_event(msg, 'ERROR')
            raise KeyError(msg)
        return db_cls

    def get_backup_location(self, frmt):
        t = utils.get_time('%Y-%m-%d_%H-%M')
        cr = self.count_run
        name = self.name.replace(' ', '-')
        return f'db__{t}__{name}__{self.id}-{cr}.{frmt}'

    def get_additional_args(self):
        args = []
        if not self.additional_args:
            return args
        for arg in self.additional_args.split('|'):
            if not arg:
                continue
            args.append(arg)
        return args


class DJFile(models.Model):
    name = models.CharField(max_length=200)
    dir = models.TextField()

    def save_temp_compress(self, base_dir_name):
        dest = f'{base_dir_name}/file__{self.name}.zip'
        utils.zip_item(self.dir, dest)
        utils.log_event('DJFile `%s` temp file created in `%s`' % (self.name, dest), 'debug')

    def save_temp(self, base_dir_name):
        utils.copy_item(self.dir, base_dir_name)
        utils.log_event('DJFile `%s` temp file created in `%s`' % (self.name, base_dir_name), 'debug')


class DJBackUpStorageResult(models.Model):
    STATUS = (
        ('successful', _('Successful')),
        ('unsuccessful', _('Unsuccessful')),
    )

    status = models.CharField(max_length=12, choices=STATUS)
    storage = models.ForeignKey('DJStorage', on_delete=models.SET_NULL, null=True, blank=True)
    backup_name = models.TextField()
    out = models.TextField(null=True, blank=True)
    temp_location = models.TextField(null=True, blank=True)
    size = models.PositiveIntegerField()  # (bytes)
    time_taken = models.FloatField(default=0)  # (seconds)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.storage.name} - {self.backup_name} - {self.created_at}'

    def delete_temp_file(self):
        if not self.temp_location:
            return
        try:
            utils.delete_item(self.temp_location)
            utils.log_event('Temp file `%s` deleted successfully!' % self.temp_location, 'debug')
        except OSError:
            utils.log_event('Error in delete temp file `%s` ' % self.temp_location, 'warning', exc_info=True)

    def get_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')

    def get_download_link(self):
        if self.get_local_file_path():
            return reverse_lazy('dj_backup:backup__result_download', args=(self.id,))
        return None

    def get_local_file_path(self):
        if self.status != 'successful':
            return
        if self.temp_location and utils.file_is_exists(self.temp_location):
            return self.temp_location
        storage = getattr(self, 'storage', None)
        if not storage:
            return
        if not storage.name == 'LOCAL':
            return
        if utils.file_is_exists(self.out):
            return self.out
        return None


class DJStorage(models.Model):
    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def storage_class(self):
        s = storages.STORAGES_AVAILABLE_DICT.get(self.name)
        if not s:
            return None
        return s

    def is_available(self):
        if self.storage_class in storages.STORAGES_AVAILABLE:
            return True
        return False

    def get_usage_size(self):
        return self.djbackupstorageresult_set.all().aggregate(total=models.Sum('size'))['total'] or 0


class TaskSchedule(models.Model):
    task_id = models.CharField(max_length=300)
    func = models.TextField()
    seconds = models.PositiveBigIntegerField()
    repeats = models.IntegerField(default=-1)  # '-1' forever
    count_run = models.IntegerField(default=0, editable=False)
    kwargs = models.JSONField(null=True, blank=True)
    args = models.TextField(null=True, blank=True)

    last_run = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_id

    @property
    def is_available(self):
        if self.repeats < 0:
            return True
        if self.repeats > self.count_run:
            return True
        return False

    @property
    def is_available_for_run(self):
        if DJBackUpBase.objects.filter(schedule_task=self).exists():
            return True
        return False
