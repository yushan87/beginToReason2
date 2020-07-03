"""
This module contains our Django views for the "tutor" application.
"""
from django.shortcuts import render
from accounts.models import UserInformation


def catalog(request):
    """function catalog This function handles the view for the catalog page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if request.user.is_authenticated:
        return render(request, "tutor/catalog.html",
                      {'name': UserInformation.objects.get(user_email=request.user.email).user_name})
    else:
        return render(request, "tutor/catalog.html")


def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if request.user.is_authenticated:
        '''
        query lessonset table
        get first lesson from set
        '''
        return render(request, "tutor/tutor.html",
                      {'name': UserInformation.objects.get(user_email=request.user.email).user_name})
    else:
        return render(request, "accounts/login.html")
