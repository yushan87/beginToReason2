"""
This module contains our Django views for the "tutor" application.
"""
import asyncio
import json
import re

from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data, finished_lesson_count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from educator.models import Assignment
from educator.py_helper_functions.educator_helper import assignment_auth
from tutor.py_helper_functions.mutation import can_mutate
from tutor.py_helper_functions.tutor_helper import user_auth, browser_response, replace_previous, send_to_verifier, \
    clean_variable

User = get_user_model()


@login_required(login_url='/accounts/login/')
def grader(request):
    """function grader This function handles checking code sent by the JS.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        JsonResponse: A JSON response informing the browser of the results and the user's current state
    """

    # Case 1: We have received a POST request submitting code (needs a lot of work)
    if request.method == 'POST':
        # Case 1a: if the user exists
        if user_auth(request):
            data = json.loads(request.body.decode('utf-8'))
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=data['assignment'])
            current_lesson_set, _, current_lesson, _, is_alternate = assignment.get_user_lesson(current_user.id)

            # Get submitted answer. No 'Confirm', no spaces, each ends with a semicolon
            submitted_answer = re.findall("Confirm [^;]*;|ensures [^;]*;", data['code'])
            submitted_answer = ''.join(submitted_answer)

            # Send student code file to RESOLVE verifier
            status, lines, vcs, completion_time = asyncio.run(send_to_verifier(data['code']))
            
            # Log data
            log_data(current_user, assignment, current_lesson_set, current_lesson, is_alternate, data, status,
                     vcs, completion_time)

            if status == "success":
                # Update assignment progress
                # Can use return value from advance_user to communicate to browser that assignment is completed
                assignment.advance_user(current_user.id)
                return JsonResponse(browser_response(current_lesson, assignment, current_user, submitted_answer,
                                                     status, lines, True, False))
            else:
                # Activate alternate if needed
                changed = assignment.alternate_check(current_user.id, data['code'])
                return JsonResponse(browser_response(current_lesson, assignment, current_user, submitted_answer,
                                                     status, lines, changed, changed))
    return redirect("accounts:profile")


def tutor(request, assignmentID):
    """function tutor This function handles giving code to the browser.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        assignmentID (Integer): ID of the assignment that the user is requesting code for
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if request.method == 'GET':
        if assignment_auth(request, assignmentID):
            # Case 2a: User is valid and is taking this assignment
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=assignmentID)
            _, set_index, current_lesson, _, is_alternate = \
                assignment.get_user_lesson(current_user.id)
            num_done = finished_lesson_count(current_user)

            if current_lesson.is_parsons:
                return redirect('parsons:parsons', assignmentID)

            # Just as we are altering the code here with mutate, this will pull the previous answer
            # to put in place for sub lessons. What identifiers do we need?

            current_lesson.code.lesson_code = can_mutate(current_lesson)
            current_lesson.code.lesson_code = replace_previous(current_user, current_lesson.code.lesson_code,
                                                               is_alternate)
            current_lesson.code.lesson_code = clean_variable(current_lesson.code.lesson_code)

            # Case 2aa: if questions if MC or Both
            if current_lesson.reason.reasoning_type in ('MC', 'Both'):
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'reason': current_lesson.reason.reasoning_question,
                               'mc_set': current_lesson.reason.mc_set.all(),
                               'setLength': assignment.main_set.length(),
                               'finished_count': num_done,
                               'orderedSet': assignment.main_set.sets(),
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': set_index,
                               'isParsons': current_lesson.is_parsons})
            # Case 2ab: if question is of type Text
            elif current_lesson.reason.reasoning_type == 'Text':
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'reason': current_lesson.reason.reasoning_question,
                               'setLength': assignment.main_set.length(),
                               'finished_count': num_done,
                               'orderedSet': assignment.main_set.sets(),
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': set_index,
                               'isParsons': current_lesson.is_parsons})

            # Case 2ac: if question is of type none
            return render(request, "tutor/tutor.html",
                          {'lesson': current_lesson,
                           'assignment': assignment,
                           'lesson_code': current_lesson.code.lesson_code,
                           'concept': current_lesson.lesson_concept.all(),
                           'referenceSet': current_lesson.reference_set.all(),
                           'setLength': assignment.main_set.length(),
                           'finished_count': num_done,
                           'orderedSet': assignment.main_set.sets(),
                           'mood': current_user.mood,
                           'review': 'none',
                           'screen_record': current_lesson.screen_record,
                           'audio_record': current_lesson.audio_record,
                           'audio_transcribe': current_lesson.audio_transcribe,
                           'user_email': request.user.email,
                           'index': set_index,
                            'isParsons': current_lesson.is_parsons})
    return redirect("accounts:profile")
