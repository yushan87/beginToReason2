"""
This module contains our Django views for the "accounts" application.
"""
from django.shortcuts import render, redirect
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


def profile(request):
    """function profile This function handles the view for the profile page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if request.user.is_authenticated:
        return render(request, "accounts/profile.html",
                      {'name': UserInformation.objects.get(user_email=request.user.email).user_name})
    else:
        return redirect(request, "accounts/login.html")


@csrf_protect
def settings(request):
    """function settings This function handles the view for the account settings page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # Case 1: User has logged in and has been properly authenticated
    if request.user.is_authenticated:
        # Case 1a: We have received a POST request with some data
        if request.method == 'POST':
            form = CreateUser(request.POST)
            # Case 1aa: A valid user profile form
            if form.is_valid():
                form.save()
                request.session.set_expiry(0)
                return redirect(request, "accounts/profile.html")
            # Case 1ab: Not a valid user profile form, render the settings page with the form (empty else block)
        # Case 1b: We have received something other than a POST request
        else:
            # Case 1ba: The user email exists in our user information table.
            if UserInformation.objects.filter(user_email=request.user.email).exists():
                # Case 1baa: The user information has all the required fields filled in.
                if UserInformation.objects.get(user_email=request.user.email).user_name == "" or \
                        UserInformation.objects.get(user_email=request.user.email).user_school == "" or \
                        UserInformation.objects.get(user_email=request.user.email).user_class == "" or \
                        UserInformation.objects.get(user_email=request.user.email).user_gender == "" or \
                        UserInformation.objects.get(user_email=request.user.email).user_race == "":
                    form = CreateUser(initial={'user_email': request.user.email})
                    form.save()
                request.session.set_expiry(0)
                return render(request, "accounts/profile.html",
                              {'name': UserInformation.objects.get(user_email=request.user.email).user_name})
                # Case 1bab: This user profile has missing information that needs to be filled in,
                #            we render the settings page with the form (empty else block)
            # Case 1bb: The user email doesn't exist in our user information table,
            #           we render the settings page with the form (empty else block)
            form = CreateUser(initial={'user_email': request.user.email})

        # Return statement for case 1ab, 1bab and 1bb
        return render(request, "accounts/settings.html", {'form': form})
    # Case 2: User needs to log in
    else:
        return render(request, "accounts/login.html")


def logout(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    """
    return
