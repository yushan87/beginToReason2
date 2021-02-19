"""
This module contains model templates for the "accounts" application. In particular, it contains templates for the
database tables related to the user account information. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from core.models import LessonSet, MainSet


class UserInformation(models.Model):
    """
    Contains a model of a user to keep track of user information.
    """
    # All of the fields in the model has validators to make sure they are valid.
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Foreign key referring to an entry in the user table
    user_nickname = models.CharField("Nickname", max_length=25, validators=[MinLengthValidator(1)])  # Nickname field
    user_school = models.CharField("School", max_length=100, validators=[MinLengthValidator(1)])  # School field
    user_class = models.CharField("Class", max_length=100, validators=[MinLengthValidator(1)])  # Class name field
    user_gender = models.CharField("Gender", max_length=50, validators=[MinLengthValidator(1)])  # Gender field
    user_race = models.CharField("Race", max_length=50, validators=[MinLengthValidator(1)])  # Race field
    current_main_set = models.ForeignKey(MainSet, blank=True, on_delete=models.CASCADE, null=True)
    current_lesson_set = models.ForeignKey(LessonSet, blank=True, on_delete=models.CASCADE, null=True)
    current_lesson_index = models.IntegerField(default=0)
    completed_lesson_index = models.IntegerField(default=0)
    current_lesson_name = models.CharField(max_length=200, default="None")
    completed_sets = models.ForeignKey(MainSet, on_delete=models.CASCADE, blank=True, related_name='sets_completed', null=True)
    mood = models.CharField(max_length=10, default="neutral")

    def __str__(self):
        """function __str__ is used to create a string representation of this class

        Returns:
            str: user email
        """
        return self.user.email

    def get_user_email(self):
        """function get_user_email is an helper function to retrieve the email associated with the user

        Returns:
            str: user email
        """
        return self.user.email
    get_user_email.short_description = 'User Email'  # Renames column head
