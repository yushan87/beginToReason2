"""
This module contains our Django views for the "accounts" application.
"""
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import UserInformation
from .forms import CreateUser


def login(request):
    """function login This function handles the view for the login page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "accounts/login.html")


@csrf_protect
def profile(request):
    """function profile This function handles the view for the profile page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                form.save()
                request.session.set_expiry(0)
                return render(request, "accounts/settings.html")
        else:
            if UserInformation.objects.filter(user_email=request.user.email).exists():
                if UserInformation.objects.filter(user_email=request.user.email).values('user_name') == "" or \
                        UserInformation.objects.filter(user_email=request.user.email).values('user_school') == "" or \
                        UserInformation.objects.filter(user_email=request.user.email).values('user_class') == "" or \
                        UserInformation.objects.filter(user_email=request.user.email).values('user_gender') == "" or \
                        UserInformation.objects.filter(user_email=request.user.email).values('user_race') == "":
                    form = CreateUser(initial={'user_email': request.user.email})
                    form.save()
                # print(UserInformation.objects.filter(user_email=request.user.email).values())
                request.session.set_expiry(0)
                return render(request, "accounts/settings.html")
            form = CreateUser(initial={'user_email': request.user.email})
        return render(request, "accounts/profile.html", {'form': form})
    else:
        return render(request, "accounts/login.html")


def settings(request):
    """function settings This function handles the view for the account settings page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if request.user.is_authenticated:
        return render(request, "accounts/settings.html")
    else:
        return render(request, "accounts/login.html")


def logout(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    """
    return
