# Generated by Django 4.2 on 2024-08-08 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0017_djdatabasebackup_additional_args_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='djdatabasebackup',
            old_name='database_name',
            new_name='database_type',
        ),
    ]
