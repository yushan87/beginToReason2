"""
This module contains our Django views for the "tutor" application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Lesson


def catalog(request):
    """function catalog This function handles the view for the catalog page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    return render(request, "tutor/catalog.html")


@login_required(login_url='/accounts/login/')
def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # Case 1: We have received a POST request with some data
    if request.method == 'POST':
        print("\n\n\n\n********** in post **********\n\n\n\n")
        # hook up websocket and verify
        # if success, return next lesson
        # if fail, do something
        if Lesson.objects.filter(lesson_name='lesson2').exists():
            current_lesson = Lesson.objects.get(lesson_name='lesson2')
            return render(request, "tutor/tutor.html",
                          {'lessonName': current_lesson.lesson_title,
                           'concept': current_lesson.lesson_concept,
                           'instruction': current_lesson.instruction,
                           'code': current_lesson.code.lesson_code,
                           'referenceSet': current_lesson.reference_set.all(),
                           'reason': current_lesson.reason.reasoning_question})
        else:
            return render(request, "tutor/tutor.html")

    # Case 2: Load a current lesson (need to track what lesson user is on)
    else:
        # need a check for if lesson exists
        if Lesson.objects.filter(lesson_name='lesson1').exists():
            current_lesson = Lesson.objects.get(lesson_name='lesson1')
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
            else:
                print(current_lesson.reason.reasoning_type)
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
            return render(request, "tutor/tutor.html")
