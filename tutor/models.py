"""
This module contains model templates for the "tutor" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.db import models

# Create your models here.


class CodeTemplate(models.Model):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    template_name = models.CharField(max_length=30)
    template_code = models.TextField(max_length=500)

    def __str__(self):
        """function __str__ TODO: Need to fill in the correct information for this function.

        Returns:
            str: TODO: Need to fill in the correct information for this function.
        """
        return self.template_name


class Lesson(models.Model):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    lesson_name = models.CharField(max_length=30)
    lesson_code = models.TextField(max_length=500)
    template = CodeTemplate

    def __str__(self):
        """function __str__ TODO: Need to fill in the correct information for this function.

        Returns:
            str: TODO: Need to fill in the correct information for this function.
        """
        return self.lesson_name


class Reference(models.Model):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    reference_key = models.CharField(max_length=30)
    reference_text = models.TextField(max_length=250)
    lesson = models.ManyToManyField(Lesson, related_name='references')
       # , through= 'LessonReferences')

    def __str__(self):
        """function __str__ TODO: Need to fill in the correct information for this function.

        Returns:
            str: TODO: Need to fill in the correct information for this function.
        """
        return self.reference_key
