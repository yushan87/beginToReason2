"""
This module contains model templates for the "instructor" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.core.validators import MinLengthValidator
from django.db import models

from accounts.models import UserInformation
from core.models import MainSet


class Class(models.Model):
    """
    A model of a class

    @param models.Model The base model
    """
    class_name = models.CharField("Name", max_length=100, validators=[MinLengthValidator(1)])  # Class name field
    main_sets = models.ManyToManyField(MainSet, blank=True, related_name='classes')  # Sets assigned to the class
    join_code = models.CharField("Join_Code", max_length=6, validators=[MinLengthValidator(6)], unique=True)  # Code for joining class

    def __str__(self):
        """function __str__ is used to create a string representation of this class

        Returns:
            str: user email
        """
        return self.class_name

    def user_count(self):
        """function user_count is used to count how many students are in a class

        Returns:
            int: count of how many non-instructor users are enrolled
        """
        return ClassMembership.objects.filter(class_taking_id=self.id, is_instructor=False).count()


class ClassMembership(models.Model):
    """
    A many-to-many containing a boolean signifying whether user is instructor of class or not

    @param models.Model The base model
    """
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    class_taking = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
