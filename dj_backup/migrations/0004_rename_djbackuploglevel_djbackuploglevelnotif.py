# Generated by Django 5.2.1 on 2025-07-10 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0003_rename_t_djbackupsecure_encryption_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DJBackupLogLevel',
            new_name='DJBackupLogLevelNotif',
        ),
    ]
