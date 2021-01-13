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
    print("Set not complete: ", request)
    if current_user.current_lesson_set is None:
        return False

    current_set = current_user.current_lesson_set.lessons.all()
    if current_set.exists():

        if request.method == 'POST':
            print("Not complete call from POST")
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
            print("Not complete call from GET")
            if current_user.current_lesson_index < len(current_set):
                print("TEST PRINT")
                return True
    return False


def not_complete(request):
    print("not_complete method in tutor_helper.py")
    if user_auth(request):
        user = User.objects.get(email=request.user.email)
        print("\t", user)
        current_user = UserInformation.objects.get(user=user)
        print("\t", current_user)
        print("\tCurrent Lesson Set: ", current_user.current_lesson_set )
        print("\tCompleted Lesson Sest: ", current_user.completed_sets.all())

        if current_user.current_lesson_set not in current_user.completed_sets.all():
            print("not complete")
            return True
    return False

def alternate_lesson_check(current_lesson, type):
    """function set_not_complete This function handles the logic for a if a set has not been completed

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        String: name of lesson to redirect to
    """

    dict = { 'NUM' : current_lesson.use_of_concrete_values,
             'INIT': current_lesson.not_using_initial_value,
             'SIM' : current_lesson.simplify,
             'SELF': current_lesson.self_reference,
             'ALG' : current_lesson.algebra,
             'VAR' : current_lesson.variable,
             'DEF' : current_lesson.lesson_name
    }

    if current_lesson.sub_lessons_available:
        return Lesson.objects.get(lesson_name=dict[type])

    return current_lesson



def check_type(current_lesson, submitted_answer, status):
    all_answers = submitted_answer.split(";")
    type = 'None'

    queried_set = current_lesson.incorrect_answers.all()
    for ans in all_answers:
        search = ans + ';'
        for each in queried_set:
            if search == each.answer_text:
                print(search)
                type = each.answer_type
                break

    if type == 'None' and status == 'failure':
        type = 'DEF'
    elif type == 'None':
        type = 'COR'

    return type


def check_status(status):
    if status == 'success':
        return True
    return False


def check_feedback(current_lesson, submitted_answer, status):
    type = 'DEF'

    if status == 'success':
        headline = 'Correct'
        text = current_lesson.correct_feedback
        type = 'COR'
    else:
        if current_lesson.sub_lessons_available:

            type = check_type(current_lesson, submitted_answer, status)

            try:
                headline = current_lesson.feedback.get(feedback_type=type).headline
                text = current_lesson.feedback.get(feedback_type=type).feedback_text
            except:
                type = 'DEF'
            finally:
                headline = current_lesson.feedback.get(feedback_type=type).headline
                text = current_lesson.feedback.get(feedback_type=type).feedback_text
        else:
            if status == 'failure':
                headline = current_lesson.feedback.get(feedback_type='DEF').headline
                text = current_lesson.feedback.get(feedback_type='DEF').feedback_text
                type = 'DEF'
            else:
                return{'resultsHeader': "<h3>Something went wrong</h3>",
                       'resultDetails': 'Try again or contact us.',
                       'status': status}

    return {'resultsHeader': headline,
            'resultDetails': text,
            'status': status,
            'sub': current_lesson.sub_lessons_available,
            'type': type,
            }

