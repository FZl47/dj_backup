from django import forms

from . import models


class DJFileBackUpForm(forms.ModelForm):
    class Meta:
        model = models.DJFileBackUp
        fields = '__all__'


class DJFileForm(forms.ModelForm):
    class Meta:
        model = models.DJFile
        fields = '__all__'



