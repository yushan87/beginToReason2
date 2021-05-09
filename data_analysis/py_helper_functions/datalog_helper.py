"""
This module contains our Django helper functions for the "data analysis" application.
"""
import json
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import UserInformation
from core.models import LessonSet, Lesson
from data_analysis.models import DataLog
from tutor.py_helper_functions.mutation import reverse_mutate


def log_data(request):
    """function log_data This function handles the logic for logging data
    Args:
         request (HTTPRequest): A http request object created automatically by Django.
    Returns:
    """
    user = User.objects.get(email=request.user.email)
    user_info = UserInformation.objects.get(user=user)
    lesson_set = user_info.current_lesson_set
    main_set = user_info.current_main_set
    lesson = Lesson.objects.get(lesson_name=user_info.current_lesson_name)
    if lesson.can_mutate:
        original_code = reverse_mutate(json.loads(request.body.decode('utf-8'))['code'])
    else:
        original_code = json.loads(request.body.decode('utf-8'))['code']

    code = json.loads(request.body.decode('utf-8'))['code']
    explanation = json.loads(request.body.decode('utf-8'))['explanation']
    past_answers = json.loads(request.body.decode('utf-8'))['allAnswers']
    status = json.loads(request.body.decode('utf-8'))['status']
    face = json.loads(request.body.decode('utf-8'))['face']
    user_info.mood = face
    user_info.save()

    print("data_logged")

    data_to_log = DataLog.objects.create(user_key=user,
                                         time_stamp=timezone.now(),
                                         lesson_set_key=lesson_set,
                                         assignment_key=main_set,
                                         lesson_key=lesson,
                                         status=status,
                                         code=code,
                                         explanation=explanation,
                                         face=face,
                                         original_code=original_code)
    data_to_log.save()


def get_log_data(user, lesson_name):
    """function get_log_data This function handles getting log data

    Args:
        user: the user model for who we are looking for logs
        lesson_name: the name of the Lesson

    Returns:
        String representation of data log
    """
    user = User.objects.get(email=user)
    print(user)
    get_user_successes = DataLog.objects.filter(user_key=user)
    print(get_user_successes)

    print("[][][][]", get_user_successes.filter(lesson_set_key=LessonSet.objects.get(set_name=lesson_name)))
    get_lesson = get_user_successes.filter(lesson_set_key=LessonSet.objects.get(set_name=lesson_name)).order_by('-id')[0]

    print(get_lesson)
    return repr(get_lesson.code).replace("'",''), get_lesson.face, get_lesson.past_answers, get_lesson.explanation


def finished_lesson_count(user):
    """function finished_lesson_count This function returns the number of finished lesson by the user

    Args:
        user: the user model for who we are looking for log count

    Returns:
        int of successes found in the logs by the user
    """
    user = User.objects.get(email=user)

    get_user_successes = DataLog.objects.filter(user_key=user).filter(status='success')
    print(get_user_successes.count())

    return get_user_successes.count()
