import abc

from django_q.models import Schedule

from dj_backup.core.backup.file import FileBackup
from dj_backup.core import utils
from dj_backup import models


class ScheduleBackupBaseTask(abc.ABC):
    _func_run = None
    test_run = True

    def __init__(self, backup_obj):
        self.backup_obj = backup_obj
        if self.test_run:
            self.test()
            return
        st = Schedule.objects.create(
            name='schedule_backup_task_%s' % backup_obj.name,
            schedule_type='I',
            repeats=backup_obj.repeats,
            minutes=backup_obj.convert_unit_interval_to_minute(),
            kwargs={'backup_obj_id': backup_obj.id},
            func=self._func_run,
        )

        backup_obj.schedule_task = st
        backup_obj.save()

    @staticmethod
    @abc.abstractmethod
    def run(backup_obj_id, *args, **kwargs):
        raise NotImplementedError

    def test(self):
        self.run(backup_obj_id=self.backup_obj.id)


class ScheduleFileBackupTask(ScheduleBackupBaseTask):
    _func_run = 'dj_backup.core.tasks.ScheduleFileBackupTask.run'

    @staticmethod
    def run(backup_obj_id, *args, **kwargs):
        try:
            backup_obj = models.DJFileBackUp.objects.get(id=backup_obj_id)
            if backup_obj.has_running_task:
                utils.log_event('Backup(`%s`) has currently running task' % backup_obj_id, 'warning', exc_info=True)
                return
        except models.DJFileBackUp.DoesNotExist:
            utils.log_event('DJFileBackup object not found. object id `%s`' % backup_obj_id, 'error', exc_info=True)
            return

        """
            To solve the problem of interference between two or more tasks, the `has_running_task` variable is used 
            so that it does not interfere when a task takes longer than the time of the next task.
        """
        backup_obj.has_running_task = True
        backup_obj.save(update_fields=['has_running_task'])

        fb = FileBackup(backup_obj)

        def handler():
            """It can take a long time"""
            file_path = fb.get_backup()
            storages = backup_obj.get_storages()
            for storage_obj in storages:
                storage = storage_obj.storage_class(backup_obj, file_path)
                # add time taken backup to storage
                storage.time_taken += fb.time_taken
                storage.save()
            """End"""

        try:
            handler()
        except Exception:
            pass
        finally:
            backup_obj.count_run += 1
            backup_obj.has_running_task = False
            backup_obj.save()

        # delete raw temp file
        fb.delete_raw_temp()
        if not backup_obj.has_temp:
            backup_obj.delete_temp_files()

        # delete task when the count number reaches 0
        if backup_obj.schedule_task:
            if backup_obj.schedule_task.repeats == 0:
                backup_obj.schedule_task.delete()
                return


class ScheduleDataBaseBackupTask(ScheduleBackupBaseTask):
    _func_run = 'dj_backup.core.tasks.ScheduleDataBaseBackupTask.run'

    @staticmethod
    def run(backup_obj_id, *args, **kwargs):
        try:
            backup_obj = models.DJDataBaseBackUp.objects.get(id=backup_obj_id)
            if backup_obj.has_running_task:
                utils.log_event('Backup(`%s`) has currently running task' % backup_obj_id, 'warning', exc_info=True)
                return
        except models.DJDataBaseBackUp.DoesNotExist:
            utils.log_event('DJDataBaseBackUp object not found. object id `%s`' % backup_obj_id, 'error', exc_info=True)
            return

        db_instance = backup_obj.db_ins
        if not db_instance:
            return

        """
            To solve the problem of interference between two or more tasks, the `has_running_task` variable is used 
            so that it does not interfere when a task takes longer than the time of the next task.
        """
        backup_obj.has_running_task = True
        backup_obj.save(update_fields=['has_running_task'])

        def handler():
            """It can take a long time"""
            # create export dump file
            file_path = db_instance.get_backup()
            storages = backup_obj.get_storages()
            for storage_obj in storages:
                storage = storage_obj.storage_class(backup_obj, file_path)
                # add time taken backup to storage
                storage.time_taken += db_instance.time_taken
                storage.save()
            """End"""

        try:
            handler()
        except Exception:
            pass
        finally:
            backup_obj.count_run += 1
            backup_obj.has_running_task = False
            backup_obj.save()

        # delete raw temp file
        db_instance.delete_dump_file()
        if not backup_obj.has_temp:
            backup_obj.delete_temp_files()

        # delete task when the count number reaches 0
        if backup_obj.schedule_task:
            if backup_obj.schedule_task.repeats == 0:
                backup_obj.schedule_task.delete()
                return
