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
    user_class = models.CharField("Class", max_length=100, validators=[MinLengthValidator(1)])  # Class name field
