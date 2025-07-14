import abc

from typing import Optional, Union

from pathlib import Path

from dj_backup.core.backup.file import FileBackup
from dj_backup.core import utils, task, logging
from dj_backup.core.utils import secure
from dj_backup import models


class ScheduleBackupBaseTask(abc.ABC):
    test_run: bool = False
    backup_obj = Optional[Union[models.DJFileBackUp, models.DJDataBaseBackUp]]

    def __init__(self, backup_obj: Union[models.DJFileBackUp, models.DJDataBaseBackUp], strict: bool = True) -> None:
        """
            Abstract base class for scheduling backup tasks.

            This class provides a framework for creating scheduled backup tasks.
            It initializes the backup task and allows for testing without scheduling.

            Args:
                backup_obj: The backup object to be scheduled.
                strict (bool): Whether to enforce strict scheduling (default is True).

            Attributes:
                backup_obj: The backup object to be scheduled.
                test_run (bool): Indicates whether the task is a test run (default is False).

            Methods:
                run(backup_obj_id: int, *args, **kwargs) -> None:
                    Abstract method to run the backup task. Must be implemented by subclasses.
                    This method should contain the logic for performing the backup operation,
                    such as saving data, encryption, or any other processing related to backing up.
                test() -> None:
                    Test the backup task by running it without scheduling.
        """

        self.backup_obj = backup_obj
        if self.test_run:
            self.test()
            return

        task_id = backup_obj.get_task_id()
        st = task.TaskSchedule(
            self.run,
            backup_obj.convert_unit_interval_to_seconds(),
            backup_obj.repeats,
            strict=strict,
            task_id=task_id,
            f_kwargs={'backup_obj_id': backup_obj.id}
        )

        backup_obj.schedule_task = st.task_obj
        backup_obj.save()

    @staticmethod
    @abc.abstractmethod
    def run(backup_obj_id: int, *args, **kwargs) -> None:
        """
            Run the backup task.

            Args:
                backup_obj_id (int): The ID of the backup object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
        """
        raise NotImplementedError

    def test(self) -> None:
        """
            Test the backup task by running it without scheduling.
        """
        self.run(backup_obj_id=self.backup_obj.id)


class ScheduleFileBackupTask(ScheduleBackupBaseTask):

    @staticmethod
    def run(backup_obj_id: int, *args: list, **kwargs: dict) -> None:
        """
            Run the file backup task.

            Args:
                backup_obj_id (int): The ID of the file backup object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
        """
        try:
            backup_obj = models.DJFileBackUp.objects.get(id=backup_obj_id)
            if backup_obj.has_running_task:
                utils.log_event('Backup(`%s`) has currently running task' % backup_obj_id, 'warning', exc_info=True)
                return
        except models.DJFileBackUp.DoesNotExist:
            utils.log_event('DJFileBackup object not found. object id `%s`' % backup_obj_id, 'error', exc_info=True)
            return

        backup_obj.has_running_task = True
        backup_obj.save(update_fields=['has_running_task'])

        fb = FileBackup(backup_obj)

        def handler():
            """It can take a long time"""
            file_path = fb.get_backup()
            file_path = Path(file_path)

            _enc_manager = None

            backup_sec = backup_obj.get_secure()
            if backup_sec:
                _enc_manager = secure.get_enc_by_name(backup_sec.encryption_type)
                _enc_manager = _enc_manager()
                file_path_encrypted = _enc_manager.save(file_path, key=backup_sec.key)

                if file_path_encrypted:
                    fb.delete_zip_temp()
                    file_path = file_path_encrypted
                else:
                    _enc_manager = None

            storages = backup_obj.get_storages()
            for storage_obj in storages:
                storage = storage_obj.storage_class(backup_obj, file_path)
                storage.time_taken += fb.time_taken
                storage.save()

            fb.delete_raw_temp()
            if not backup_obj.has_temp:
                if _enc_manager:
                    _enc_manager.delete_temp_files()
                else:
                    fb.delete_zip_temp()
            """End"""

        try:
            handler()
        except Exception as e:
            logging.log_event('There is some problem in schedule file backup task [%s]' % e.__str__(), 'ERROR',
                              exc_info=True)
        finally:
            backup_obj.count_run += 1
            backup_obj.has_running_task = False
            backup_obj.save()


class ScheduleDataBaseBackupTask(ScheduleBackupBaseTask):

    @staticmethod
    def run(backup_obj_id: int, *args: list, **kwargs: dict) -> None:
        """
            Run the database backup task.

            Args:
                backup_obj_id (int): The ID of the database backup object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
        """
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

        backup_obj.has_running_task = True
        backup_obj.save(update_fields=['has_running_task'])

        def handler():
            """It can take a long time"""
            file_path = db_instance.get_backup()
            file_path = Path(file_path)

            _enc_manager = None

            backup_sec = backup_obj.get_secure()
            if backup_sec:
                _enc_manager = secure.get_enc_by_name(backup_sec.encryption_type)
                _enc_manager = _enc_manager()
                file_path_encrypted = _enc_manager.save(file_path, key=backup_sec.key)

                if file_path_encrypted:
                    db_instance.delete_zip_temp()
                    file_path = file_path_encrypted
                else:
                    _enc_manager = None

            storages = backup_obj.get_storages()
            for storage_obj in storages:
                storage = storage_obj.storage_class(backup_obj, file_path)
                storage.time_taken += db_instance.time_taken
                storage.save()

            db_instance.delete_dump_file()
            if not backup_obj.has_temp:
                if _enc_manager:
                    _enc_manager.delete_temp_files()
                else:
                    db_instance.delete_zip_temp()
            """End"""

        try:
            handler()
        except Exception as e:
            logging.log_event('There is some problem in schedule database backup task [%s]' % e.__str__(), 'ERROR',
                              exc_info=True)
        finally:
            backup_obj.count_run += 1
            backup_obj.has_running_task = False
            backup_obj.save()
