"""
This module contains our Django helper functions for the "data analysis" application.
"""
import json
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import UserInformation
from core.models import LessonSet, Lesson
from data_analysis.models import DataLog


def log_data(request):
    """function log_data This function handles the logic for logging data

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
    """
    user = User.objects.get(email=request.user.email)
    user_info = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
    lesson_set = user_info.current_lesson_set
    set_array = lesson_set.lessons.all()
    lesson = Lesson.objects.get(lesson_name=set_array[user_info.current_lesson_index])
    code = json.loads(request.body.decode('utf-8'))['code']
    explanation = json.loads(request.body.decode('utf-8'))['explanation']
    status = json.loads(request.body.decode('utf-8'))['status']

    data_to_log = DataLog.objects.create(user_key=user,
                                         time_stamp=timezone.now(),
                                         lesson_set_key=lesson_set,
                                         lesson_key=lesson,
                                         status=status,
                                         code=code,
                                         explanation=explanation)
    data_to_log.save()
