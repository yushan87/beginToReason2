"""
This module contains our Django helper functions for the "tutor" application.
"""
import json
import re
import urllib
import websockets

from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import UserInformation
from core.models import LessonSet, Lesson, MainSet
from instructor.models import Assignment, AssignmentProgress, ClassMembership
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


def assignment_auth(request):
    """function lesson_auth This function handles the auth logic for an assignment

    Args:
         request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        Boolean: A boolean to signal if the student is able to go into the assignment
    """
    if user_auth(request):
        # Do we have the assignment in the DB?
        if Assignment.objects.filter(id=request.POST.get("assignment_id")).exists():
            print("HIT")
            assignment = Assignment.objects.get(id=request.POST.get("assignment_id"))
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))

            # Is the user already taking this assignment?
            if AssignmentProgress.objects.filter(assignment_key=assignment, user_info_key=current_user).exists():
                print("old assignment")
                # I should include a completed assignment check here. Is this how it works?
                progress = AssignmentProgress.objects.get(assignment_key=assignment, user_info_key=current_user)
                if progress.current_lesson_index == progress.completed_lesson_index:
                    print("Already completed!")
                    return False
                return True
            else:
                # Is the user in the class for this assignment?
                if ClassMembership.objects.filter(user=current_user, class_taking=assignment.class_key).exists():
                    progress = AssignmentProgress(user_info_key=current_user, assignment_key=assignment,
                                                  current_lesson_set=assignment.main_set.lessons.all()[0],
                                                  current_lesson_index=0, completed_lesson_index=-1)
                    progress.save()
                    print("starting new assignment")
                    return True
                print("User not in the class for this assignment!")
        else:
            print("Assignment doesn't exist!")
    else:
        print("Bad user!")
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


def alternate_lesson_check(current_lesson, type):
    """function alternate_lesson_check This function handles the logic for a if a lesson has an alternate

    Args:
         current_lesson: a Lesson that is currently being completed
         type: type of lesson to use for lookup

    Returns:
        current_lesson: a Lesson found from finding alternate with lookup of type
    """
    dict = {'NUM': current_lesson.use_of_concrete_values,
            'INIT': current_lesson.not_using_initial_value,
            'SIM': current_lesson.simplify,
            'SELF': current_lesson.self_reference,
            'ALG': current_lesson.algebra,
            'VAR': current_lesson.variable,
            'DEF': current_lesson.default
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
                return {'resultsHeader': "<h3>Something went wrong</h3>",
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

    for i in range(0, occurrence):
        if last_attempt.find("Read(", index) != -1:
            index = last_attempt.find("Read(", index) + 5
            variables.append(last_attempt[index])
            index = index + 1

    print(variables)

    for i in range(0, len(variables)):
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
                indices1.append(last_attempt.find(';', index1) + 1)
                index1 = indices1[i + 1] + 1

                indices2.append(code.find('Confirm', index2))
                index2 = indices2[i] + 1
                indices2.append(code.find(';', index2) + 1)
                index2 = indices2[i + 1] + 1

        old_strings = []
        new_strings = []

        for i in range(0, len(indices1), 2):
            old_strings.append(last_attempt[indices1[i]:indices1[i + 1]])
            new_strings.append(code[indices2[i]:indices2[i + 1]])

        for i in range(0, len(old_strings)):
            code = code.replace(new_strings[i], old_strings[i])

    return code


async def send_to_verifier(code):
    async with websockets.connect(
            'wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project', ping_interval=None) as ws:
        await ws.send(encode(code))

        while True:
            response = json.loads(await ws.recv())
            if response['status'] == 'complete':
                return response


def encode(data):
    """
        Don't ask, just accept. This is how the Resolve Web API works at the
        moment. If you want to fix this, PLEASE DO.
    """
    print("orig:", data)
    data = urllib.parse.quote(data)
    print("parsed:", data)
    re.sub(" ", "%20", data)
    re.sub("/+", "%2B", data)
    print("replaced:", data)
    return json.dumps({'name': 'BeginToReason', 'pkg': 'User', 'project': 'Teaching_Project', 'content': data,
                       'parent': 'undefined', 'type': 'f'})
