"""
This module contains our Django views for the "tutor" application.
"""
import asyncio
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Lesson, LessonSet
from accounts.models import UserInformation
import json
from django.http import JsonResponse
from tutor.py_helper_functions.tutor_helper import user_auth, lesson_set_auth, set_not_complete
from tutor.py_helper_functions.websocket_helper import hello


def catalog(request):
    """function catalog This function handles the view for the catalog page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # get all lesson sets, display
    if request.method == 'POST':
        if user_auth(request):
            # search for lesson set
            if lesson_set_auth(request):
                return redirect("/tutor/tutor")
            else:
                return redirect("accounts:profile")
        else:
            return redirect("/accounts/settings")
    else:
        print("calling catalog")
        return render(request, "tutor/catalog.html", {'LessonSet': LessonSet.objects.all()})


@login_required(login_url='/accounts/login/')
def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # Case 1: We have received a POST request submitting code (needs a lot of work)
    if request.method == 'POST':
        '''
        This is a temporary FAKED verifer
        '''
        # Case 1a: if the user exists
        if user_auth(request):
            submitted_json = json.loads(request.body)
            # hook up websocket and verify
            # if success, return next lesson
            # if fail, do something
            # Case 1aa: if the user has not completed set
            if set_not_complete(request):
                print("calling server")
                hello()
                return JsonResponse({'status': 'success'})
            # Case 1ab: if the user has not completed set
            else:
                # this would mean it was the last lesson in the set
                # remove lesson set from user in whatever relationship a user has with lesson sets TBD
                return redirect("accounts:profile")
        # Case 1b: if the user doesnt exist
        else:
            return redirect("accounts:settings")
    # Case 2: We have received a GET request requesting code
    elif request.method == 'GET':
        # Ensure user exists
        # Case 2a: if the user exists
        if user_auth(request):
            # Case 2aa: if the user has a current set
            if set_not_complete(request):
                current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
                current_set = current_user.current_lesson_set.lessons.all()
                # Case 2aaa: if the current set has a lesson of index that the user is on, set to current lesson
                if Lesson.objects.filter(lesson_name=current_set[current_user.current_lesson_index]).exists():
                    current_lesson = Lesson.objects.get(lesson_name=current_set[current_user.current_lesson_index])
                    # Case 2aaaa: if the question is of type MC
                    if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                        return render(request, "tutor/tutor.html",
                                      {'lessonName': current_lesson.lesson_title,
                                       'concept': current_lesson.lesson_concept.all(),
                                       'instruction': current_lesson.instruction,
                                       'code': current_lesson.code.lesson_code,
                                       'referenceSet': current_lesson.reference_set.all(),
                                       'reason': current_lesson.reason.reasoning_question,
                                       'reason_type': current_lesson.reason.reasoning_type,
                                       'mc_set': current_lesson.reason.mc_set.all(),
                                       'screen_record': current_lesson.screen_record})
                    # Case 2aaab: if question is of type Text
                    elif current_lesson.reason.reasoning_type == 'Text':
                        return render(request, "tutor/tutor.html",
                                      {'lessonName': current_lesson.lesson_title,
                                       'concept': current_lesson.lesson_concept.all(),
                                       'instruction': current_lesson.instruction,
                                       'code': current_lesson.code.lesson_code,
                                       'referenceSet': current_lesson.reference_set.all(),
                                       'reason': current_lesson.reason.reasoning_question,
                                       'reason_type': current_lesson.reason.reasoning_type,
                                       'screen_record': current_lesson.screen_record})
                    else:
                        # need something for if there is no question
                        return redirect("accounts:profile")
                # Case 2aab: if the current lesson doesnt exist, this would mean set could be complete
                else:
                    # Do something more here
                    return redirect("accounts:profile")
                    # Case 2aab: if the current lesson doesnt exist, this would mean set could be complete
            # Case 2ab: the user does not have a current set, send them to get one
            else:
                return redirect("accounts:profile")
        # Case 2b: if the user doesnt exist, redirect to settings
        else:
            return redirect("accounts:settings")
