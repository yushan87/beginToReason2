"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms
from .models import UserInformation, Class


class UserInformationForm(forms.ModelForm):
    """
    This form creates an instance of a UserInformation model and collects its fields
    """
    # Special options
    blank = ''
    prefer = 'Prefer Not To Answer'

    # School options
    clemson = 'Clemson University'
    fau = 'Florida Atlantic University'
    osu = 'The Ohio State University'
    rhit = 'Rose-Hulman Institute of Technology'
    other = 'Other'
    schools = [
        (blank, ''),
        (clemson, 'Clemson University'),
        (fau, 'Florida Atlantic University'),
        (osu, 'The Ohio State University'),
        (rhit, 'Rose-Hulman Institute of Technology'),
        (other, 'Other')
    ]

    # Gender options
    male = 'Male'
    female = 'Female'
    genders = [
        (blank, ''),
        (male, 'Male'),
        (female, 'Female'),
        (prefer, 'Prefer Not To Answer')
    ]

    # Race options
    native = 'American Indian or Alaska Native'
    asian = 'Asian'
    black = 'Black or African American'
    hispanic = 'Hispanic or Latino'
    hawaiian = 'Native Hawaiian or Other Pacific Islander'
    white = 'White'
    races = [
        (blank, ''),
        (native, 'American Indian or Alaska Native'),
        (asian, 'Asian'),
        (black, 'Black or African American'),
        (hispanic, 'Hispanic or Latino'),
        (hawaiian, 'Native Hawaiian or Other Pacific Islander'),
        (white, 'White'),
        (prefer, 'Prefer Not To Answer')
    ]

    # Fields that will need to be completed in this form
    user_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'readonly': 'readonly'}))  # read only
    user_nickname = forms.CharField(label='Nickname', max_length=25)
    user_school = forms.ChoiceField(label='School', choices=schools)
    user_class = forms.ModelChoiceField(label='Class', queryset=Class.objects.all())
    user_gender = forms.ChoiceField(label='Gender', choices=genders)
    user_race = forms.ChoiceField(label='Race', choices=races)
    user_instructor = forms.BooleanField(label='Are You An Instructor?', required=True)

    def __init__(self, *args, **kwargs):
        """function __init__ is called to instantiate the user information form

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # super(UserInformationForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

        # Validator that makes sure all the fields have been filled in
        for _field_name, field in self.fields.items():
            field.required = True

    class Meta:
        """
        A class that stores the meta information about this form
        """
        model = UserInformation
        fields = ['user_email', 'user_nickname', 'user_school', 'user_class', 'user_gender', 'user_race', 'user_instructor']
