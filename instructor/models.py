"""
This module contains model templates for the "instructor" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.core.validators import MinLengthValidator
from django.db import models


class Class(models.Model):
    """
    A model of a class

    @param models.Model The base model
    """
    class_name = models.CharField("Class", max_length=100, validators=[MinLengthValidator(1)])  # Class name field

    def __str__(self):
        """function __str__ is used to create a string representation of this class

        Returns:
            str: user email
        """
        return self.class_name
