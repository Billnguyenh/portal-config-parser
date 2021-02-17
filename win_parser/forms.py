from django import forms
from .models import WindowsConfigFile

class WindowsConfigFileForm(forms.ModelForm):
    config_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta: 
        model = WindowsConfigFile
        fields = ['config_file']

