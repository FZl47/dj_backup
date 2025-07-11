from .base import (
    DJBackUpBase, DJFileBackUp, DJDataBaseBackUp, DJBackUpStorageResult, DJBackupSecure, DJStorage, DJFile, TaskSchedule
)
from .notification import *


def get_backup_object(backup_id):
    return DJBackUpBase.objects.get_subclass(id=backup_id)


__all__ = [
    'DJBackUpBase', 'DJFileBackUp', 'DJDataBaseBackUp', 'DJBackupSecure',
    'DJBackupLog', 'DJBackupLogLevelNotif', 'TaskSchedule',
    'DJBackUpStorageResult', 'DJStorage', 'DJFile',
    'get_backup_object',
]
