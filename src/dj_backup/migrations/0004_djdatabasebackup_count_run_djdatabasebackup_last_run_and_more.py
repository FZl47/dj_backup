# Generated by Django 4.2 on 2024-08-04 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_q', '0014_schedule_cluster'),
        ('dj_backup', '0003_djfile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='djdatabasebackup',
            name='count_run',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='djdatabasebackup',
            name='last_run',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='djdatabasebackup',
            name='schedule_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_q.schedule'),
        ),
        migrations.AddField(
            model_name='djfilebackup',
            name='count_run',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='djfilebackup',
            name='last_run',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='djfilebackup',
            name='schedule_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_q.schedule'),
        ),
    ]