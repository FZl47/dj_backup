# Generated by Django 4.2 on 2024-08-10 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0021_remove_djbackupstorageresult_backup_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DJBackupErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('exc', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='djdatabasebackup',
            name='err_logs',
            field=models.ManyToManyField(blank=True, to='dj_backup.djbackuperrorlog'),
        ),
        migrations.AddField(
            model_name='djfilebackup',
            name='err_logs',
            field=models.ManyToManyField(blank=True, to='dj_backup.djbackuperrorlog'),
        ),
    ]