from django.db.models.signals import pre_delete
from django.dispatch import receiver

from dj_backup.core.task.schedule import StorageTask

from . import models


def delete_backup_handler(backup_obj):
    # delete tasks
    backup_obj.delete_tasks()
    # delete results and temp file
    results = backup_obj.results.all()
    for result in results:
        result.delete_temp_file()
        result.delete()


@receiver(pre_delete, sender=models.DJFileBackUp)
def delete_dj_file_backup_handler(sender, instance, **kwargs):
    delete_backup_handler(instance)


@receiver(pre_delete, sender=models.DJDataBaseBackUp)
def delete_dj_file_backup_handler(sender, instance, **kwargs):
    delete_backup_handler(instance)


@receiver(pre_delete, sender=models.TaskSchedule)
def delete_task_job_handler(sender, instance, **kwargs):
    StorageTask.remove_task_by_id(instance.task_id)
