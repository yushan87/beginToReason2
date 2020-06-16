"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms
from .models import UserInformation


class CreateUser(forms.ModelForm):
    """
    This form creates an instance of a UserInformation model and collects its fields
    """
    blank = ''
    clemson = 'Clem'
    fau = 'FAU'
    rhit = 'RHIT'
    other = 'Other'
    schools = [
        (blank, ''),
        (clemson, 'Clemson'),
        (fau, 'FAU'),
        (rhit, 'RHIT'),
        (other, 'Other')
    ]

    cpsc2150 = 'CPSC2150'
    cpsc3720 = 'CPSC3720'
    classes = [
        (blank, ''),
        (cpsc2150, 'CPSC2150'),
        (cpsc3720, 'CPSC3720'),
        (other, 'Other')
    ]

    male = 'Male'
    female = 'Female'
    prefer = 'Prefer Not To Answer'
    genders = [
        (blank, ''),
        (male, 'Male'),
        (female, 'Female'),
        (prefer, 'Prefer Not To Answer')
    ]

    na = 'American Indian or Alaska Native'
    asian = 'Asian'
    black = 'Black or African American'
    hispanic = 'Hispanic or Latino'
    hawaiian = 'Native Hawaiian or Other Pacific Islander'
    white = 'White'
    races = [
        (blank, ''),
        (na, 'American Indian or Alaska Native'),
        (asian, 'Asian'),
        (black, 'Black or African American'),
        (hispanic, 'Hispanic or Latino'),
        (hawaiian, 'Native Hawaiian or Other Pacific Islander'),
        (white, 'White'),
        (prefer, 'Prefer Not To Answer')
    ]

    # this should be not changeable / read only
    user_email = forms.EmailField(label='Email')
    user_name = forms.CharField(label='Username', max_length=100)
    user_school = forms.ChoiceField(label='School', choices=schools)
    user_class = forms.ChoiceField(label='Class', choices=classes)
    user_gender = forms.ChoiceField(label='Gender', choices=genders)
    user_race = forms.ChoiceField(label='Race', choices=races)

    class Meta:
        model = UserInformation
        fields = ['user_email', 'user_name', 'user_school', 'user_class', 'user_gender', 'user_race']
