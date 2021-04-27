"""
This module contains our Django helper functions for the "tutor" application.
"""
import json
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import UserInformation
from core.models import LessonSet, Lesson, MainSet
from tutor.models import LessonLog
from data_analysis.models import DataLog


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


def user_auth_inst(request):
    """function user_auth_inst This function handles the auth logic for an instructor in both django users and UserInformation

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the user has been found in our database
    """
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        if UserInformation.objects.filter(user=user).exists():
            inst = UserInformation.objects.get(user=user)
            if(inst.user_instructor):
                return True
    return False


def lesson_set_auth(request):
    """function lesson_auth This function handles the auth logic for a lessonSet

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the lessonSet has been found in our database
    """
    if MainSet.objects.filter(set_name=request.POST.get("set_name")).exists():
        print("HIT")
        main_set = MainSet.objects.filter(set_name=request.POST.get("set_name"))[0]
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        if current_user.completed_sets.filter(set_name=request.POST.get("set_name")).exists():
            return False
        if LessonLog.objects.filter(user=current_user.user).exists():
            print("checking for lesson log")
            log = LessonLog.objects.filter(user=current_user.user)
            print("log: ", log)
            if log.filter(main_set_key=main_set).exists():
                lesson_logs = log.filter(main_set_key=main_set).last()
                print("??????", lesson_logs.lesson_set_key.first_in_set)
                current_user.current_main_set = main_set
                current_set = LessonSet.objects.get(set_name=lesson_logs.lesson_set_key.set_name)

                if (lesson_logs.lesson_index + 1) < len(main_set.lessons.all()):
                    next_set = LessonSet.objects.get(set_name=main_set.lessons.all()[lesson_logs.lesson_index + 1])
                else:
                    next_set = LessonSet.objects.get(set_name=main_set.lessons.all()[lesson_logs.lesson_index])
                current_user.current_lesson_set = next_set
                current_user.current_lesson_name = next_set.first_in_set.lesson_name
                current_user.current_lesson_index = 0
                current_user.completed_lesson_index = 0
                current_user.mood = "neutral"
                current_user.save()
                if current_user.current_lesson_index < len(current_user.current_lesson_set.lessons.all()):
                    print("found in logs")
                    return True
        else:
            current_user.current_main_set = main_set
            print("1: ", main_set.lessons.all()[0])
            current_set = LessonSet.objects.get(set_name=main_set.lessons.all()[0])
            current_user.current_lesson_set = current_set
            print(current_set.lessons.all())
            current_user.current_lesson_name = current_set.first_in_set.lesson_name
            current_user.current_lesson_index = 0
            current_user.completed_lesson_index = 0
            current_user.mood = "neutral"
            current_user.save()
            if current_user.current_lesson_index < len(current_user.current_lesson_set.lessons.all()):
                print("starting new set")
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
    """function not_complete This function handles the logic for a if a set has not been completed

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the set has been completed
    """
    print("not_complete method in tutor_helper.py")
    if user_auth(request):
        user = User.objects.get(email=request.user.email)
        print("\t", user)
        current_user = UserInformation.objects.get(user=user)
        if current_user.current_main_set is None:
            return False
        if current_user.completed_sets is not None:
            if current_user.current_main_set not in current_user.completed_sets.all():
                print("not complete")
                print(current_user.current_main_set)
                return True
        else:
            if current_user.completed_sets is None:
                return True
    return False


def alternate_lesson_check(current_lesson, type):
    """function alternate_lesson_check This function handles the logic for a if a lesson has an alternate

    Args:
         current_lesson: a Lesson that is currently being completed
         type: type of lesson to use for lookup

    Returns:
        current_lesson: a Lesson found from finding alternate with lookup of type
    """
    dict = { 'NUM' : current_lesson.use_of_concrete_values,
             'INIT': current_lesson.not_using_initial_value,
             'SIM' : current_lesson.simplify,
             'SELF': current_lesson.self_reference,
             'ALG' : current_lesson.algebra,
             'VAR' : current_lesson.variable,
             'DEF' : current_lesson.default
    }

    if current_lesson.sub_lessons_available:
        return Lesson.objects.get(lesson_name=dict[type])

    return current_lesson


def check_type(current_lesson, submitted_answer, status):
    """function check_type This function finds the type of alternate to look for

    Args:
         current_lesson: a Lesson that is currently being completed
         submitted_answer: string of code that user submitted
        status: string of result from compiler

    Returns:
        type: type of lesson to use for lookup
    """
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
    """function check_status This function converts a string to a boolean

        Args:
            status: string of result from compiler

        Returns:
            boolean
        """
    if status == 'success':
        return True
    return False


def check_feedback(current_lesson, submitted_answer, status, unlock_next):
    """function check_feedback This function finds the feedback to show to the user

    Args:
         current_lesson: a Lesson that is currently being completed
         submitted_answer: string of code that user submitted
         status: string of result from compiler
         unlock_next: boolean for unlocking next button

    Returns:
        type: type of lesson to use for lookup
    """
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
            'unlock_next': unlock_next
            }


def log_lesson(request):
    """function log_lesson This function handles the logic for logging lessons
    Args:
         request (HTTPRequest): A http request object created automatically by Django.
    Returns:
    """
    user = User.objects.get(email=request.user.email)
    user_info = UserInformation.objects.get(user=user)
    lesson_set = user_info.current_lesson_set
    lesson = Lesson.objects.get(lesson_index=user_info.current_lesson_index)
    main_set = user_info.current_main_set

    print("lesson_logged")

    lesson_to_log = LessonLog.objects.create(user=user,
                                             time_stamp=timezone.now(),
                                             lesson_set_key=lesson_set,
                                             lesson_key=lesson,
                                             lesson_index=lesson.lesson_index,
                                             main_set_key=main_set)
    lesson_to_log.save()


def align_with_previous_lesson(user, code):
    """function align_with_previous_lesson This function changes the mutation to match the last lesson they did

    Args:
         user: user model using tutor
         code: code that user submitted in last lesson

    Returns:
        code: code with variables matching letters of that from their last lesson
    """
    last_attempt = DataLog.objects.filter(user_key=User.objects.get(email=user)).order_by('-id')[0].code

    occurrence = 3
    original = ["I", "J", "K"]
    variables = []
    index = 0

    for i in range(0,occurrence):
        if last_attempt.find("Read(", index) != -1:
            index = last_attempt.find("Read(", index) + 5
            variables.append(last_attempt[index])
            index = index + 1

    print(variables)

    for i in range(0,len(variables)):
        code = code.replace(original[i], variables[i])

    change = variables[0] + "nteger"

    code = code.replace(change, "Integer")

    change = variables[0] + "f"

    code = code.replace(change, "If")

    return code


def replace_previous(user, code, is_alt):
    """function replace_previous This function changes the previous lesson code

    Args:
         user: user model using tutor
         code: code that user submitted in last lesson
         is_alt: boolean for if alternate lesson

    Returns:
        code: ? string of code
    """
    if not DataLog.objects.filter(user_key=User.objects.get(email=user)):
        print("There is no datalog")
        return code

    if is_alt:
        code = align_with_previous_lesson(user, code)

    last_attempt = DataLog.objects.filter(user_key=User.objects.get(email=user)).order_by('-id')[0].code

    # Checks if there is code to be replaced
    present = code.find('/*previous')

    if present != -1:
        print("present")

        occurrence = 20
        indices1 = []
        indices2 = []
        index1 = 0
        index2 = 0

        # Has to identify the starting and ending index for each confirm statement. The format does differ
        # between the old and new.

        for i in range(0, occurrence, 2):
            if last_attempt.find('Confirm', index1) != -1:
                indices1.append(last_attempt.find('Confirm', index1))
                index1 = indices1[i] + 1
                indices1.append(last_attempt.find(';', index1)+1)
                index1 = indices1[i+1] + 1

                indices2.append(code.find('Confirm', index2))
                index2 = indices2[i] + 1
                indices2.append(code.find(';', index2)+1)
                index2 = indices2[i+1] + 1

        old_strings = []
        new_strings = []

        for i in range(0, len(indices1),2):
            old_strings.append(last_attempt[indices1[i]:indices1[i+1]])
            new_strings.append(code[indices2[i]:indices2[i+1]])

        for i in range(0,len(old_strings)):
            code = code.replace(new_strings[i],old_strings[i])

    return code
