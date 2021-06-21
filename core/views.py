"""
This module contains our Django views for the "core" application.
"""
from django.shortcuts import render


def home(request):
    """function home This function handles the view for the index page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "core/index.html")


def privacy(request):
    """function login This function handles the view for the privacy page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "core/privacy.html")
