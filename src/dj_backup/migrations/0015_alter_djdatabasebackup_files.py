# Generated by Django 4.2 on 2024-08-07 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0014_djdatabasebackup_database_djdatabasebackup_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='djdatabasebackup',
            name='files',
            field=models.ManyToManyField(blank=True, to='dj_backup.djfile'),
        ),
    ]
