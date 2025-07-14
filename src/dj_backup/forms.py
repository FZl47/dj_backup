from django import forms

from . import models


class DJBackupSecureForm(forms.ModelForm):
    class Meta:
        model = models.DJBackupSecure
        fields = '__all__'


class DJFileBackUpForm(forms.ModelForm):
    class Meta:
        model = models.DJFileBackUp
        exclude = ('count_run', 'has_running_task')


class DJFileBackUpUpdateForm(forms.ModelForm):
    class Meta:
        model = models.DJFileBackUp
        exclude = ('count_run', 'files', 'schedule_task', 'results', 'has_running_task')


class DJDataBaseBackUpForm(forms.ModelForm):
    class Meta:
        model = models.DJDataBaseBackUp
        exclude = ('count_run', 'has_running_task')


class DJDataBaseBackUpUpdateForm(forms.ModelForm):
    class Meta:
        model = models.DJDataBaseBackUp
        exclude = ('count_run', 'files', 'schedule_task', 'results',
                   'database', 'database_type', 'additional_args', 'has_running_task')


class DJFileForm(forms.ModelForm):
    class Meta:
        model = models.DJFile
        fields = '__all__'


class DJBackupLogLevelNotifForm(forms.ModelForm):
    class Meta:
        model = models.DJBackupLogLevelNotif
        exclude = ('is_active',)
