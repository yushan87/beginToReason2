"""
This module contains model templates for the "accounts" application. In particular, it contains templates for the
database tables related to the user account information. When we create a new item in the database,
a new instance of a model will be made.
"""
from datetime import datetime
from django.db import models

# Create your models here.


class UserInformation(models.Model):
    """
    Contains a model of a user to keep track of user information
    @param models.Model
    """
    user_email = models.EmailField()
    user_name = models.TextField()
    date_joined = models.DateTimeField(default=datetime.now())

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
    user_school = models.CharField(
        max_length=10,
        choices=schools,
        default=other
    )

    cpsc2150 = 'CPSC2150'
    cpsc3720 = 'CPSC3720'
    classes = [
        (blank, ''),
        (cpsc2150, 'CPSC2150'),
        (cpsc3720, 'CPSC3720'),
        (other, 'Other')
    ]
    user_class = models.CharField(
        max_length=10,
        choices=classes,
        default=other
    )

    male = 'Male'
    female = 'Female'
    prefer = 'Prefer Not To Answer'
    genders = [
        (blank, ''),
        (male, 'Male'),
        (female, 'Female'),
        (prefer, 'Prefer Not To Answer')
    ]
    user_gender = models.CharField(
        max_length=25,
        choices=genders,
        default=prefer
    )

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
    user_race = models.CharField(
        max_length=50,
        choices=races,
        default=prefer
    )

    def __str__(self):
        """function __str__ is called on a user to retrieve information

            Returns:
                str: user name
        """
        return self.user_name

    def getuser(self):
        """function getuser is called on a user to retrieve information

                    Returns:
                        str: user email
                """
        return self.user_email
