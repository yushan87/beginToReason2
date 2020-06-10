"""
This module is where we create and keep track of all the Django views.
"""
from django.shortcuts import render


def home(request):
    """function home This function handles the view for the index page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "app/homePage.html")


def tutor(request):
    """function home This function handles the view for the tutor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "app/lesson_template.html", {'content': "Lessons goes here!"})


def login(request):
    """function home This function handles the view for the login page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "app/login.html")

