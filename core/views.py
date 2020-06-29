"""
This module contains our Django views for the "core" application.
"""
from django.shortcuts import render
from accounts.models import UserInformation


def home(request):
    """function home This function handles the view for the index page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    if request.user.is_authenticated:
        return render(request, "core/index.html",
                      {'name': UserInformation.objects.get(user_email=request.user.email).user_name})
    else:
        return render(request, "core/index.html")
