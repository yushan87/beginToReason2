"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms

from . import models


class CreateUser(forms.ModelForm):
    """
    This form creates an instance of a UserInformation model and collects its fields
    """
    class Meta:
        model = models.UserInformation
        fields = ['user_email', 'user_id', 'user_name']
