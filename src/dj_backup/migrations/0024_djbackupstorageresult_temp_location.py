# Generated by Django 4.2 on 2024-08-11 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0023_djbackuplog_remove_djdatabasebackup_err_logs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='djbackupstorageresult',
            name='temp_location',
            field=models.TextField(blank=True, null=True),
        ),
    ]
