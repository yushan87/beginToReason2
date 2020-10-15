"""
This module contains our Django helper functions for the "tutor" application.
"""
import json
from django.contrib.auth.models import User
from accounts.models import UserInformation
from core.models import LessonSet, Lesson


def user_auth(request):
    """function user_auth This function handles the auth logic for a user in both django users and UserInformation

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the user has been found in our database
    """
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        if UserInformation.objects.filter(user=user).exists():
            return True
    return False


def lesson_set_auth(request):
    """function lesson_auth This function handles the auth logic for a lessonSet

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the lessonSet has been found in our database
    """
    if LessonSet.objects.filter(set_name=request.POST.get("set_name")).exists():
        current_set = LessonSet.objects.get(set_name=request.POST.get("set_name"))
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        current_user.current_lesson_set = current_set
        current_user.current_lesson_name = current_set.lessons.all()[0].lesson_name

        current_user.current_lesson_index = 0
        current_user.completed_lesson_index = 0
        current_user.mood = "neutral"
        current_user.save()
        if current_user.current_lesson_index < len(current_user.current_lesson_set.lessons.all()):
            return True
    return False


def lesson_auth(request):
    """function lesson_auth This function handles the auth logic for a lesson

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the lesson has been found in our database
    """


def set_not_complete(request):
    """function set_not_complete This function handles the logic for a if a set has not been completed

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the set has been completed
    """
    current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
    if current_user.current_lesson_set is None:
        return False
    current_set = current_user.current_lesson_set.lessons.all()
    if current_set.exists():
        current_set = current_user.current_lesson_set.lessons.all()
        if request.method == 'POST':
            # need a variation of what to do if the last lesson was completed
            if current_user.current_lesson_index < len(current_set) - 1:
                # increase index of lesson set depending on if user is on a previously completed lesson
                if current_user.current_lesson_index < current_user.completed_lesson_index:
                    current_user.current_lesson_index = current_user.current_lesson_index + 1
                else:
                    current_user.completed_lesson_index = current_user.completed_lesson_index + 1
                    current_user.current_lesson_index = current_user.current_lesson_index + 1
                current_user.save()
                return True
            else:
                # remove set from current set
                return False
        elif request.method == 'GET':
            if current_user.current_lesson_index < len(current_set):
                return True
    return False


def alternate_lesson_check(request):
    """function set_not_complete This function handles the logic for a if a set has not been completed

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        String: name of lesson to redirect to
    """
    submitted_answer = json.loads(request.body.decode('utf-8'))['answer'].replace(" ", "")
    current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
    current_set = current_user.current_lesson_set.lessons.all()
    if current_set.exists() and Lesson.objects.filter(lesson_name=current_user.current_lesson_name).exists():
        current_lesson = Lesson.objects.filter(lesson_name=current_user.current_lesson_name)[0]
        if current_lesson.sub_lessons_available:
            queried_set = current_lesson.incorrect_answers.all()
            for incorrect in queried_set:
                if submitted_answer == incorrect.answer_text:
                    if incorrect.answer_type == 'SIM':
                        current_user.current_lesson_name = current_lesson.simplify
                        current_user.save()
                    elif incorrect.answer_type == 'SELF':
                        current_user.current_lesson_name = current_lesson.self_reference
                        current_user.save()
                    elif incorrect.answer_type == 'NUM':
                        current_user.current_lesson_name = current_lesson.use_of_concrete_values
                        current_user.save()
                    elif incorrect.answer_type == 'INIT':
                        current_user.current_lesson_name = current_lesson.not_using_initial_value
                        current_user.save()
                    elif incorrect.answer_type == 'ALG':
                        current_user.current_lesson_name = current_lesson.algebra
                        current_user.save()
                    elif incorrect.answer_type == 'VAR':
                        current_user.current_lesson_name = current_lesson.variable
                        current_user.save()
    return True


def select_feedback(request):
    submitted_answer = json.loads(request.body.decode('utf-8'))['answer'].replace(" ", "")
    current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
    current_set = current_user.current_lesson_set.lessons.all()
    if current_set.exists() and Lesson.objects.filter(lesson_name=current_user.current_lesson_name).exists():
        current_lesson = Lesson.objects.filter(lesson_name=current_user.current_lesson_name)[0]
        queried_set = current_lesson.incorrect_answers.all()
        feedback_set = current_lesson.feedback.all()
        if not queried_set:
            return feedback_set.get(feedback_type='DEF')
        else:
            for each in queried_set:
                if submitted_answer == each.answer_text:
                    return feedback_set.get(feedback_type=each.answer_type)
        return feedback_set.get(feedback_type='COR')
    return False