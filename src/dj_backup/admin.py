from django.contrib import admin

from dj_backup import models

admin.site.register(models.DJFileBackUp)
admin.site.register(models.DJDataBaseBackUp)
admin.site.register(models.DJBackupSecure)
admin.site.register(models.DJFile)
admin.site.register(models.DJStorage)
admin.site.register(models.DJBackUpStorageResult)

admin.site.register(models.TaskSchedule)

admin.site.register(models.DJBackupLog)
admin.site.register(models.DJBackupLogLevelNotif)
