"""
This module contains model templates for the "accounts" application. In particular, it contains templates for the
database tables related to the user account information. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

import educator

User = get_user_model()


class UserInformation(models.Model):
    """
    Contains a model of a user to keep track of user information.
    """
    # All of the fields in the model has validators to make sure they are valid.
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Foreign key referring to an entry in the user table
    user_nickname = models.CharField("Nickname", max_length=25, validators=[MinLengthValidator(1)])  # Nickname field
    user_school = models.CharField("School", max_length=100, validators=[MinLengthValidator(1)])  # School field
    user_gender = models.CharField("Gender", max_length=50, validators=[MinLengthValidator(1)])  # Gender field
    user_race = models.CharField("Race", max_length=50, validators=[MinLengthValidator(1)])  # Race field
    user_educator = models.BooleanField(default=False)  # Whether user can create classes, view educator tools
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

    def get_current_assignments(self):
        """function get_current_assignments is an helper function to retrieve a user's non-completed assignments

        Returns:
            Array: List of all assignments user has started but has not completed
        """
        assignments = []
        for progress in educator.models.AssignmentProgress.objects.filter(user_info_key=self, current_set_index__gt=-1):
            assignments.append(progress.assignment_key)
        return assignments

    def get_completed_assignments(self):
        """function get_completed_assignments is an helper function to retrieve a user's completed assignments

        Returns:
            Array: List of all assignments user has started and has not completed
        """
        assignments = []
        for progress in educator.models.AssignmentProgress.objects.filter(user_info_key=self, current_set_index=-1):
            # Check that there's no alternate lessons
            if educator.models.AlternateProgress.objects.filter(progress=progress).count() == 0:
                # No alternate lessons either, add to the list
                assignments.append(progress.assignment_key)
        return assignments

    get_user_email.short_description = 'User Email'  # Renames column head
