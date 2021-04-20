"""
This module contains our forms for the "instructor" application.
"""
from django import forms


class NewClassForm(forms.Form):
    class_name = forms.CharField(label='Class name', max_length=30)
