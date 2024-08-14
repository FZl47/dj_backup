# Generated by Django 4.2 on 2024-08-10 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0022_djbackuperrorlog_djdatabasebackup_err_logs_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DJBackupLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=40)),
                ('exc', models.TextField()),
                ('is_seen', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='djdatabasebackup',
            name='err_logs',
        ),
        migrations.RemoveField(
            model_name='djfilebackup',
            name='err_logs',
        ),
        migrations.DeleteModel(
            name='DJBackupErrorLog',
        ),
    ]