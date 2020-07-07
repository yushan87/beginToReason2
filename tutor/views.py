"""
This module contains our Django views for the "tutor" application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
    lesson1 = Lesson.objects.get(lesson_name='testLesson')
    print(lesson1.reference_set.all())
    return render(request, "tutor/tutor.html",
                  {'lessonName': lesson1.lesson_name,
                   'concept': lesson1.lesson_concept,
                   'instruction': lesson1.instruction,
                   'code': lesson1.code,
                   'referenceSet': lesson1.reference_set,
                   'reason': lesson1.reason})
