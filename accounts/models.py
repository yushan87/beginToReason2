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
    user_school = models.CharField(max_length=50)
    user_class = models.CharField(max_length=50)
    user_gender = models.CharField(max_length=50)
    user_race = models.CharField(max_length=50)

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
