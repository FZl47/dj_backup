from django import forms

from . import models


class DJFileBackUpForm(forms.ModelForm):
    class Meta:
        model = models.DJFileBackUp
        exclude = ('count_run',)


class DJFileBackUpUpdateForm(forms.ModelForm):
    class Meta:
        model = models.DJFileBackUp
        exclude = ('count_run', 'files', 'schedule_task', 'results')


class DJDataBaseBackUpForm(forms.ModelForm):
    class Meta:
        model = models.DJDataBaseBackUp
        exclude = ('count_run',)


class DJDataBaseBackUpUpdateForm(forms.ModelForm):
    class Meta:
        model = models.DJDataBaseBackUp
        exclude = ('count_run', 'files', 'schedule_task', 'results',
                   'database', 'database_type', 'additional_args')


class DJFileForm(forms.ModelForm):
    class Meta:
        model = models.DJFile
        fields = '__all__'
