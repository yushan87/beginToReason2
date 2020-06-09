"""
This module contains our Django views for the "tutor" application.
"""
from django.shortcuts import render


def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if request.user.is_authenticated:
        return render(request, "tutor/lesson_template.html")
    else:
        return render(request, "accounts/login.html")
