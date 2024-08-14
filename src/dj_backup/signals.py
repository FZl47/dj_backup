from django.db.models.signals import pre_delete
from django.dispatch import receiver

from . import models


def delete_backup_handler(instance):
    # delete schedule task
    if instance.schedule_task: instance.schedule_task.delete()
    # delete results
    instance.results.all().delete()


@receiver(pre_delete, sender=models.DJFileBackUp)
def delete_dj_file_backup_handler(sender, instance, **kwargs):
    delete_backup_handler(instance)


@receiver(pre_delete, sender=models.DJDataBaseBackUp)
def delete_dj_file_backup_handler(sender, instance, **kwargs):
    delete_backup_handler(instance)
