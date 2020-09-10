"""
This module contains our Django views for the "tutor" application.
"""
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Lesson, LessonSet
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data
from tutor.py_helper_functions.tutor_helper import user_auth, lesson_set_auth, set_not_complete, alternate_lesson_check


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
        # Case 1a: if the user exists
        if user_auth(request):
            # submitted_json = json.loads(request.body.decode('utf-8'))
            log_data(request)
            # if success, return next lesson
            # if fail, do something
            # Case 1aa: if the user has not completed set
            status = json.loads(request.body.decode('utf-8'))['status']
            if status == "success":
                if set_not_complete(request):
                    return render(request, "tutor/tutor.html")
                # Case 1ab: if the user has not completed set
            else:
                # this is where we will check the answer for alternate lesson
                alternate_lesson_check(request)
                return render(request, "tutor/tutor.html")
        # Case 1b: if the user doesnt exist
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
                    # log_item = DataLog.objects.get(user_key=User.objects.get(email=request.user.email),
                    # status="success", lesson_key=Lesson.objects.get(
                    # lesson_name=current_set[current_user.current_lesson_index])).code
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
                                       'screen_record': current_lesson.screen_record,
                                       'currLessonNum': current_user.current_lesson_index + 1,
                                       'completedLessonNum': current_user.completed_lesson_index + 1,
                                       'setLength': len(current_set),
                                       'currSet': current_set})
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
                                       'screen_record': current_lesson.screen_record,
                                       'currLessonNum': current_user.current_lesson_index + 1,
                                       'completedLessonNum': current_user.completed_lesson_index + 1,
                                       'setLength': len(current_set),
                                       'currSet': current_set})
    return redirect("accounts:profile")


@login_required(login_url='/accounts/login/')
def previous(request):
    """function previous This function handles retrieving the prev lesson.

        Args:
            request (HTTPRequest): A http request object created automatically by Django.

        Returns:
            HttpResponse: A generated http response object to the request depending on whether or not
                          the user is authenticated.
        """
    if request.method == 'GET':
        if user_auth(request):
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            current_set = current_user.current_lesson_set.lessons.all()
            if current_user.current_lesson_index != 0:
                current_user.current_lesson_index = current_user.current_lesson_index - 1
                current_user.save()
                if Lesson.objects.filter(lesson_name=current_set[current_user.current_lesson_index]).exists():
                    current_lesson = Lesson.objects.get(lesson_name=current_set[current_user.current_lesson_index])
                    # log_item = DataLog.objects.get(user_key=User.objects.get(email=request.user.email),
                    # status="success", lesson_key=Lesson.objects.get(
                    # lesson_name=current_set[current_user.current_lesson_index])).code
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
                                       'screen_record': current_lesson.screen_record,
                                       'currLessonNum': current_user.current_lesson_index + 1,
                                       'completedLessonNum': current_user.completed_lesson_index + 1,
                                       'setLength': len(current_set),
                                       'currSet': current_set})
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
                                       'screen_record': current_lesson.screen_record,
                                       'currLessonNum': current_user.current_lesson_index + 1,
                                       'completedLessonNum': current_user.completed_lesson_index + 1,
                                       'setLength': len(current_set),
                                       'currSet': current_set})
    return redirect("accounts:profile")
