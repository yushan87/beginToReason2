"""
This module contains our Django helper functions for the "tutor" application.
"""
import json
import re
import time
import urllib
import websockets

from django.contrib.auth.models import User

import core.models
from accounts.models import UserInformation
from core.models import Lesson
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


def alternate_set_check(current_lesson, alternate_type):
    """function alternate_set_check This function handles the logic for a if a lesson has an alternate
    Args:
         current_lesson: a Lesson that is currently being completed
         alternate_type: type of lesson to use for lookup, enum found in core.models.LessonAlternate. Supports None,
         in which case it will simply return None for the alternate lesson.
    Returns:
        LessonAlternate model, or None if no redirect needed
    """
    if alternate_type is None:
        # Nothing triggered, so nothing to activate
        return None
    try:
        # Obvious attempt
        return core.models.LessonAlternate.objects.get(lesson=current_lesson, type=alternate_type)
    except core.models.LessonAlternate.DoesNotExist:
        if alternate_type != core.models.AlternateType.DEFAULT:
            try:
                # If what I was searching for type-wise doesn't exist as an alternate option, try the default
                print("Lesson", current_lesson, "activated a type of", alternate_type, "but didn't supply a lesson to "
                                                                                       "redirect to!")
                return core.models.LessonAlternate.objects.get(lesson=current_lesson,
                                                               type=core.models.AlternateType.DEFAULT)
            except core.models.LessonAlternate.DoesNotExist:
                pass
    # If all else fails, don't redirect
    return None


def check_type(current_lesson, submitted_code):
    """function check_type This function finds the type of alternate to look for.
    Only to be called on incorrect answers.
    Args:
         current_lesson (Lesson): lesson that is currently being completed
         submitted_code (String): all the code submitted to RESOLVE, mutated in the form presented to user
    Returns:
        type: type of lesson to use for lookup (integer enumeration). Default if no incorrect answers were triggered.
    """
    for answer in get_confirm_lines(reverse_mutate(submitted_code)):
        try:
            return core.models.IncorrectAnswer.objects.get(answer_text=answer, lesson=current_lesson).type
        except core.models.IncorrectAnswer.DoesNotExist:
            continue

    return core.models.AlternateType.DEFAULT


def browser_response(current_lesson, current_assignment, current_user, submitted_answer, status, lines, unlock_next,
                     alt_activated):
    """function browser_response This function finds the feedback to show to the user
    Args:
         current_lesson: a Lesson that is currently being completed
         current_assignment: The assignment containing the lesson
         current_user: The UserInfo that is attempting the lesson
         submitted_answer: string of code that user submitted
         status: string of result from compiler
         lines: array of confirms and their statuses
         unlock_next: boolean for unlocking next button
         alt_activated: boolean changing feedback for whether a wrong answer has activated an alternate
    Returns:
        dict that should be send to front-end JS
    """

    print(status)
    print(current_lesson.code.lesson_code)

    if not alt_activated:
        if status == 'success':
            headline = 'Correct'
            text = current_lesson.correct_feedback
        else:
            try:
                if current_lesson.is_parsons:
                    headline = "Try Again!"
                    if status == "error":
                        text = "The code fragments are producing a syntax error. Ensure that if/else statments and loops have and end statement to complete them and they have content."
                    else:
                        text = "Code fragments in your program are wrong, or in wrong order. Move, remove, or replace fragments to meet the highlighted incorrect confirm statements."
                else: 
                    feedback = current_lesson.feedback.get(feedback_type=check_type(current_lesson, submitted_answer))
                    headline = feedback.headline
                    text = feedback.feedback_text
            except core.models.Feedback.DoesNotExist:
                headline = "Try Again!"
                text = "Did you read the reference material?"
    else:
        headline = "ALT!"
        text = "[explanation about alt, directions to hit next lesson]"

    return {'resultsHeader': headline,
            'resultDetails': text,
            'status': status,
            'lines': lines,
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
    """
    Sends a string to RESOLVE verifier and interprets its response.
    @param code: A string that the user submitted through the browser
    @return: Tuple defined as (status string, lines dict, vcs dict, time taken)
    """
    async with websockets.connect(
            'wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project', ping_interval=None) \
            as ws:
        start_time = time.time()
        await ws.send(encode(code))
        vcs = {}  # vc ID to 'success' or 'failure'
        vcs_info = {}  # vc IDs to actual strings of results for data logging
        while True:
            response = json.loads(await ws.recv())
            if response.get('status') == 'error':
                # Need to do some crazy stuff because of the way RESOLVE's errors work
                lines = []
                for error_dict in response['errors']:
                    for error_dict_sub in error_dict['errors']:
                        error_dict_sub['error']['msg'] = decode(error_dict_sub['error']['msg'])
                        unique = True
                        line_num = error_dict_sub['error']['ln']
                        for line in lines:
                            if line['lineNum'] == line_num:
                                unique = False
                                break
                        if unique:
                            lines.append({'lineNum': line_num, 'status': 'failure'})
                return 'error', lines, response['errors'], time.time() - start_time
            if response.get('status') is None:
                return 'failure', None, '', time.time() - start_time
            if response['status'] == 'processing':
                result = response['result']
                vcs_info[result['id']] = result['result']
                if re.search(r"^Proved", result['result']):
                    vcs[result['id']] = 'success'
                else:
                    vcs[result['id']] = 'failure'
            if response['status'] == 'complete':
                response['result'] = decode_json(response['result'])
                lines = overall_status(response, vcs)
                join_vc_info(response['result']['vcs'], vcs_info)
                return response['status'], lines, response['result']['vcs'], time.time() - start_time


def join_vc_info(vcs, vcs_info):
    """
    Joins the vcs from RESOLVE's final response with the info from each of the processing responses for data logging
    @param vcs: VCS from RESOLVE's final response
    @param vcs_info: Dict of VC IDs to VC info generated from processing responses
    @return: None
    """
    for vc in vcs:
        vc['result'] = vcs_info[vc.get('vc')]


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
    return data


def decode_json(data):
    return json.loads(decode(data))


def overall_status(data, vcs):
    """
    Takes RESOLVE's response along with the processing VCs, updates the status to be 'success' or 'failure',
    and returns an array of lines and their statuses.
    @param data: RESOLVE's final response
    @param vcs: dict made from the processing responses from RESOLVE
    @return: individual line status array
    """
    overall = 'success'
    lines = {}
    for vc in data['result']['vcs']:
        if vcs.get(vc.get('vc')) != 'success':
            overall = 'failure'
        if lines.get(vc.get('lineNum')) != 'failure':  # Don't overwrite an already failed line
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


def clean_variable(variable):
    """
    Makes a string safe to use in an HTML template by escaping newlines
    @param variable: A string (most likely code submitted by user)
    @return: Escaped string
    """
    variable = re.sub("\r\n", r"\\r\\n", variable)
    variable = re.sub("\r", r"\\r", variable)
    return re.sub("\n", r"\\n", variable)