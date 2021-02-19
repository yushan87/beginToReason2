"""
This module contains model templates for the "data_analysis" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from core.models import Lesson, LessonSet, MainSet


class DataLog(models.Model):
    """
    Contains a model of data to log, will be used every submit.

    @param models.Model The base model
    """
    # submission_id = models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)
    user_key = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=datetime.now, blank=True)
    lesson_key = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True)
    lesson_set_key = models.ForeignKey(LessonSet, on_delete=models.CASCADE, blank=True)
    main_set_key = models.ForeignKey(MainSet, blank=True, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50)
    code = models.TextField(default="null")
    explanation = models.TextField()
    past_answers = models.TextField(default="null")
    face = models.TextField(default="null")
    original_code = models.TextField(default="null")

    def __str__(self):
        """
        function __str__ is called to display the user related to the log

        Returns:
            str: status
        """
        return str(self.user_key) + ": " + self.status + " - "+ str(self.lesson_key)
