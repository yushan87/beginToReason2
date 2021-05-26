"""
This module contains our Django views for the "tutor" application.
"""
import json
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from core.models import MainSet
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data, finished_lesson_count
from educator.models import Class, ClassMembership, Assignment
from educator.py_helper_functions.educator_helper import get_classes, user_in_class_auth, assignment_auth
from tutor.py_helper_functions.tutor_helper import user_auth, browser_response, replace_previous
from tutor.py_helper_functions.mutation import can_mutate

User = get_user_model()


def catalog(request):
    """function catalog This function handles the view for the catalog page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # get all lesson sets, display
    return render(request, "tutor/catalog.html", {'LessonSet': MainSet.objects.all()})


@login_required(login_url='/accounts/login/')
def classes(request):
    """function catalog This function handles the view for the classes page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if user_auth(request):
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        if request.method == 'POST':
            # Handle class join
            class_code = request.POST.get('class-code', None)
            if class_code is not None:
                try:
                    class_to_join = Class.objects.get(join_code=class_code)
                except Class.DoesNotExist:
                    class_to_join = None
                if class_to_join is not None:
                    if ClassMembership.objects.filter(user_id=current_user.id,
                                                      class_taking_id=class_to_join.id).exists():
                        messages.error(request, "You are already in " + str(class_to_join) + "!")
                    else:
                        new_relation = ClassMembership(user_id=current_user.id, class_taking_id=class_to_join.id,
                                                       is_educator=False)
                        new_relation.save()
                        messages.info(request, "Successfully added you to " + str(class_to_join))
                else:
                    messages.error(request, "Sorry, class code invalid!")
            else:
                messages.error(request, "Sorry, class code invalid!")
            return redirect("/tutor/classes")
        return render(request, "tutor/classes.html", {'classes': get_classes(current_user)})
    else:
        return redirect("/accounts/settings")


def class_view(request, classID):
    """function catalog This function handles the view for the class page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        classID (int): The ID of the class that's being viewed
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if user_auth(request):
        if user_in_class_auth(UserInformation.objects.get(user=User.objects.get(email=request.user.email)), classID):
            class_to_show = Class.objects.get(id=classID)
            return render(request, "tutor/assignments_student.html",
                          {'class': class_to_show})
        else:
            return redirect("/tutor/classes")
    else:
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def grader(request):
    """function grader This function handles checking code sent by the JS.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        JsonResponse: A JSON response informing the browser of the results and the user's current state
    """

    print(request)

    # Case 1: We have received a POST request submitting code (needs a lot of work)
    if request.method == 'POST':
        # Case 1a: if the user exists
        if user_auth(request):
            # if success, return next lesson
            # if fail, do something

            data = json.loads(request.body.decode('utf-8'))
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=data['assignment'])
            current_lesson_set, _, current_lesson, _, is_alternate = assignment.get_user_lesson(current_user.id)
            print("lessons in set:", current_lesson_set.lessons())
            print("my lesson:", current_lesson)
            # Get submitted answer. No 'Confirm', no spaces, each ends w/ a semicolon
            submitted_answer = re.findall("Confirm [^;]*;|ensures [^;]*;", data['code'])
            submitted_answer = ''.join(submitted_answer)

            # Send it off to the RESOLVE verifier (commented out because RESOLVE is down currently). You will need
            # to import these 3 things: asyncio (not the django.asyncio), overall_status, and send_to_verifier
            # response, vcs = asyncio.run(send_to_verifier(data['code']))
            # if response is not None:
            #     lines = overall_status(response, vcs)
            #     status = response['status']
            # else:
            #     status = 'failure'
            #     lines = []

            # Placeholder for verifier response
            status = 'success'
            # issue: Eventually uncomment line below when lines are implemented in
            # lines = [3, 5]

            # Log data
            log_data(current_user, assignment, current_lesson_set, current_lesson, is_alternate, data, status)

            if status == "success":
                # Update assignment progress
                # issue: Use return value from advance_user to communicate to browser that assignment is completed
                assignment.advance_user(current_user.id)
                return JsonResponse(browser_response(current_lesson, assignment, current_user, submitted_answer,
                                                     status, True))
            else:
                # Activate alternate if needed
                assignment.alternate_check(current_user.id, data['code'])
                return JsonResponse(browser_response(current_lesson, assignment, current_user, submitted_answer,
                                                     status, False))
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
            print("===============", num_done)
            print("in if 1 - Current lesson:", current_lesson)

            # Just as we are altering the code here with mutate, this will pull the previous answer
            # to put in place for sub lessons. What identifiers do we need?

            current_lesson.code.lesson_code = can_mutate(current_lesson)
            current_lesson.code.lesson_code = replace_previous(current_user, current_lesson.code.lesson_code,
                                                               is_alternate)

            # Case 2aa: if questions if MC or Both
            if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
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
                               'index': set_index})
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
                               'index': set_index})

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
                           'index': set_index})
    return redirect("accounts:profile")
