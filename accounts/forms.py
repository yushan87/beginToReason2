"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms
from .models import UserInformation


class CreateUser(forms.ModelForm):
    """
    This form creates an instance of a UserInformation model and collects its fields
    """
    user_email = forms.EmailField(label='email', disabled=True)
    user_name = forms.CharField(label='name', max_length=100)

    class Meta:
        model = UserInformation
        fields = ['user_email', 'user_name']
