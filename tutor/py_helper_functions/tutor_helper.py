"""
This module contains our Django helper functions for the "tutor" application.
"""
import json
import re
import urllib
import websockets

from django.utils import timezone
from django.contrib.auth.models import User

import core.models
from accounts.models import UserInformation
from core.models import LessonSet, Lesson, MainSet
from data_analysis.models import DataLog
from tutor.py_helper_functions.mutation import reverse_mutate


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


def alternate_lesson_check(current_lesson, alternate_type):
    """function alternate_lesson_check This function handles the logic for a if a lesson has an alternate

    Args:
         current_lesson: a Lesson that is currently being completed
         alternate_type: type of lesson to use for lookup, enum found in core.models.LessonAlternate. Supports None,
         in which case it will simply return None for the alternate lesson.

    Returns:
        alternate_lesson: the alternate lesson that should be redirected to or None if it doesn't exist
    """
    if alternate_type is None:
        return None
    try:
        return core.models.LessonAlternate.objects.get(lesson=current_lesson, type=alternate_type).alternate_lesson
    except core.models.LessonAlternate.DoesNotExist:
        return None


def check_type(current_lesson, submitted_code):
    """function check_type This function finds the type of alternate to look for.
    Only to be called on incorrect answers.

    Args:
         current_lesson: a Lesson that is currently being completed
         submitted_code: All the code submitted to RESOLVE, mutated in the form presented to user

    Returns:
        type: type of lesson to use for lookup (integer enumeration). None if no incorrect answers were triggered.
    """
    for answer in get_confirm_lines(reverse_mutate(submitted_code)):
        try:
            answer_id = core.models.IncorrectAnswer.objects.get(answer_text=answer).id
        except core.models.IncorrectAnswer.DoesNotExist:
            continue
        try:
            return core.models.LessonIncorrectAnswers.objects.get(lesson=current_lesson, answer_id=answer_id).type
        except core.models.LessonIncorrectAnswers.DoesNotExist:
            continue

    return None


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
    try:
        if status == 'success':
            headline = 'Correct'
            text = current_lesson.correct_feedback
            type = 'COR'
        elif status == 'failure':
            if current_lesson.sub_lessons_available:
                # This is currently broken because I need to change these to enums, not strings!!!
                type = check_type(current_lesson, submitted_answer)
                try:
                    feedback = current_lesson.feedback.get(feedback_type=type)
                    headline = feedback.headline
                    text = feedback.feedback_text
                except core.models.Feedback.DoesNotExist:
                    type = 'DEF'
                    feedback = current_lesson.feedback.get(feedback_type=type)
                    headline = feedback.headline
                    text = feedback.feedback_text
            else:
                type = 'DEF'
                feedback = current_lesson.feedback.get(feedback_type=type)
                headline = feedback.headline
                text = feedback.feedback_text
        else:
            return {'resultsHeader': "<h3>Something went wrong</h3>",
                    'resultDetails': 'Try again or contact us.',
                    'status': status}
    except core.models.Feedback.DoesNotExist:
        return {'resultsHeader': "<h3>Something went wrong</h3>",
                'resultDetails': 'Try again or contact us.',
                'status': status}

    print("\n\n\n\nRESPONSE:", headline, "text", text, status, type, unlock_next)
    return {'resultsHeader': headline,
            'resultDetails': text,
            'status': status,
            'type': type,
            'unlock_next': unlock_next
            }


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
    if not DataLog.objects.filter(user_key=User.objects.get(email=user)).exists():
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
        vcs = {}
        while True:
            response = json.loads(await ws.recv())
            if response.get('status') == 'error' or response.get('status') is None:
                return None, None
            if response['status'] == 'processing':
                result = response['result']
                if re.search(r"^Proved", result['result']):
                    vcs[result['id']] = 'success'
                else:
                    vcs[result['id']] = 'failure'
            if response['status'] == 'complete':
                response['result'] = decode(response['result'])
                return response, vcs


def encode(data):
    """
        Don't ask, just accept. This is how the Resolve Web API works at the
        moment. If you want to fix this, PLEASE DO.
    """
    return json.dumps({'name': 'BeginToReason', 'pkg': 'User', 'project': 'Teaching_Project',
                       'content': urllib.parse.quote(data), 'parent': 'undefined', 'type': 'f'})


def decode(data):
    """
        Taken straight from editorUtils.js, or at least as straight as I could.
    """
    data = urllib.parse.unquote(data)
    data = re.sub(r"%20", " ", data)
    data = re.sub(r"%2B", "+", data)
    data = re.sub(r"<vcFile>(.*)</vcFile>", r"\1", data)
    data = urllib.parse.unquote(data)
    data = urllib.parse.unquote(data)
    data = re.sub(r"\n", "", data)
    return json.loads(data)


def overall_status(data, vcs):
    """
    Takes the 'result' portion of RESOLVE's response, updates the status to be 'success' or 'failure', and returns an
    array of lines and their statuses
    @param data: RESOLVE's response['data']
    @param vcs: dict made from the processing responses from RESOLVE
    @return: individual line status array
    """
    overall = 'success'
    lines = {}
    for vc in data['result']['vcs']:
        if vcs.get(vc.get('vc')) != 'success':
            overall = 'failure'
        if lines.get(vc.get('lineNum')) != 'failure': # Don't overwrite an already failed line
            lines[vc.get('lineNum')] = vcs.get(vc.get('vc'))

    # Convert lines dict to array of dicts
    line_array = []
    for line, status in lines.items():
        line_array.append({"lineNum": line, "status": status})

    # Update response
    data['status'] = overall

    return line_array


def get_confirm_lines(code):
    """
    Takes the block of code submitted to RESOLVE and returns a list of the lines that start with Confirm or ensures,
    keeping the semicolons attached at the end, and removing all spaces (starting, ending, or in between)
    @param code: All code submitted to RESOLVE verifier
    @return: List of confirm/ensures statements, missing the confirm/ensures but with their semicolons, all spaces
    removed
    """
    # Regex explanation: [^;]* is any amount of characters that isn't a semicolon, so what this is saying is find
    # all Confirm [characters that aren't ;]; OR ensures [characters that aren't ;];
    # The parentheses tell regex what to actually return out, so the Confirm/ensures are chopped off but they did have
    # to be present for it to match
    lines = []
    for match in re.findall("Confirm ([^;]*;)|ensures ([^;]*;)", code):
        for group in match:
            if group:
                # This check gets rid of the empty matches made by having 2 group statements
                # Get rid of all spaces
                lines.append(re.sub(" ", "", group))
    return lines
