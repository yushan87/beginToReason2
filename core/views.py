"""
This module contains our Django views for the "core" application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import UserInformation
from django.contrib.auth.models import User


def home(request):
    """function home This function handles the view for the index page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "core/index.html")
