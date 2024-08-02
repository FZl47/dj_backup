import abc
from django_q.models import Schedule
from dj_backup.core.backup.file import FileBackup
from dj_backup import models


class ScheduleBackupBaseTask(abc.ABC):

    # def __init__(self, name: AnyStr, interval: int,
    #              unit: Literal['seconds', 'minutes', 'hours', 'days', 'weeks'] = 'hours', *args, **kwargs):
    #     self.name = name
    #     self.interval = interval
    #     self.unit = unit
    #     self.args = args
    #     self.kwargs = kwargs

    def hook_result(self):
        # TODO: send notification(sms,email)
        pass


class ScheduleFileBackupTask(ScheduleBackupBaseTask):
    def __init__(self, backup_obj: models.DJFileBackUp):
        Schedule.objects.create(
            name='schedule_backup_task_%s' % backup_obj.name,
            schedule_type='I',
            minutes=backup_obj.convert_unit_interval_to_minute(),
            kwargs={'backup_obj_id': backup_obj.id},
            func='dj_backup.core.tasks.ScheduleFileBackupTask.run',
        )

    @staticmethod
    def run(*args, **kwargs):
        backup_obj_id = kwargs['backup_obj_id']
        try:
            backup_obj = models.DJFileBackUp.objects.get(id=backup_obj_id)
        except models.DJFileBackUp.DoesNotExist:
            # TODO: send notification(sms,email)
            # TODO: log exception
            return

        FileBackup(backup_obj)
        # TODO: add log
        # TODO: send notification(sms,email)
