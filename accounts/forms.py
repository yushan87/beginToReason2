"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms
from .models import UserInformation


class CreateUser(forms.Form):
    """
    This form creates an instance of a UserInformation model and collects its fields
    """
    model = UserInformation
    user_email = forms.EmailField(label='email')
    user_name = forms.CharField(label='name', max_length=100)
    fields = ['user_email', 'user_id', 'user_name']
