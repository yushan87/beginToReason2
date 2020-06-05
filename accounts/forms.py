from django import forms
from . import models


class CreateUser(forms.ModelForm):
    class Meta:
        model = models.UserInformation
        fields = ['user_email', 'user_id', 'user_name']
