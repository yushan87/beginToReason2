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


def log_data(user_info, assignment, lesson_set, lesson, is_alternate, browser_data, status, vcs, completion_time):
    """function log_data This function handles the logic for logging data
    Args:
         user_info: The user that input the code
         assignment: Assignment this log was a part of
         lesson_set: Lesson set this log was a part of
         lesson: Lesson user was taking
         is_alternate: Boolean for whether lesson is an alternate or not
         browser_data: Data returned from JS (NOT RESOLVE data)
         status: Either 'success' or 'failure'
         vcs: Array containing info of RESOLVE vcs
         completion_time: Time it took for RESOLVE to verify
    """
    user = user_info.user
    if lesson.can_mutate:
        original_code = reverse_mutate(browser_data['code'])
    else:
        original_code = browser_data['code']

    code = browser_data['code']
    explanation = browser_data['explanation']
    face = browser_data['face']
    user_info.mood = face
    user_info.save()

    print("data_logged")

    data_to_log = DataLog.objects.create(user_key=user,
                                         time_stamp=timezone.now(),
                                         lesson_set_key=lesson_set,
                                         assignment_key=assignment,
                                         lesson_key=lesson,
                                         is_alternate=is_alternate,
                                         status=status,
                                         code=code,
                                         explanation=explanation,
                                         face=face,
                                         original_code=original_code,
                                         vcs=vcs,
                                         time_took=completion_time)
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
