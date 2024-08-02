from django.contrib import admin

from dj_backup import models

admin.site.register(models.DJFileBackUp)
admin.site.register(models.DJDatabaseBackUp)
admin.site.register(models.DJFile)
