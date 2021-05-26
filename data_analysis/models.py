"""
This module contains model templates for the "data_analysis" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from core.models import Lesson, LessonSet
from educator.models import Assignment

User = get_user_model()


class DataLog(models.Model):
    """
    Contains a model of data to log, will be used every submit.

    @param models.Model The base model
    """
    user_key = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=datetime.now, blank=True)
    lesson_key = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True)
    is_alternate = models.BooleanField(null=False, blank=False)
    lesson_set_key = models.ForeignKey(LessonSet, on_delete=models.CASCADE, blank=True)
    assignment_key = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50)
    code = models.TextField(default="null")
    explanation = models.TextField()
    face = models.TextField(default="null")
    original_code = models.TextField(default="null")

    def __str__(self):
        """
        function __str__ is called to display the user related to the log

        Returns:
            str: status
        """
        return str(self.user_key) + ": " + self.status + " - " + str(self.lesson_key)
