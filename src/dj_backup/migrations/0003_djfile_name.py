# Generated by Django 4.2 on 2024-07-31 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_backup', '0002_remove_djfile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='djfile',
            name='name',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
    ]