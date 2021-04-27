"""
This module contains our Django views for the "accounts" application.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import UserInformation
from .forms import UserInformationForm


def login(request):
    """function login This function handles the view for the login page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "accounts/login.html")


def logout(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return redirect("/")


def privacy(request):
    """function login This function handles the view for the privacy page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "accounts/privacy.html")


@login_required(login_url='/accounts/login/')
def profile(request):
    """function profile This function handles the view for the profile page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HTML Render of profile page or settings if user is not registered
        name: user nickname
        completedSet: list of completed lesson sets
        currentSet: current set user is working on
    """
    # Query for user in the 'User' table
    print("GET IN  ACCOUNTS PROFILE")
    user = User.objects.get(email=request.user.email)

    # Case 1: The user email exists in our user information table.
    if UserInformation.objects.filter(user=user).exists():
        # Validate that we have a proper user information model
        user_info = UserInformation.objects.get(user=user)
        try:
            user_info.full_clean()

            # Case 1a: The user information model is valid, therefore we can render the profile page.
            request.session.set_expiry(0)
            print("USER EXISTS IN ACCOUNTS   ", request.method)
            print(request)
            return render(request, "accounts/profile.html", {'name': user_info.user_nickname,
                                                             'CompletedSet': user_info.completed_sets.all(),
                                                             'CurrentSet': user_info.current_main_set})
        except ValidationError:
            # Case 1b: The user information model is invalid,
            #           we redirect to the settings page
            return redirect("/accounts/settings")
    # Case 2: The user doesn't have an entry in our user information table,
    #          we redirect to the settings page
    else:
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
@csrf_protect
def settings(request):
    """function settings This function handles the view for the account settings page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HTML Render of settings page
        form: user information form for registering a user with some prepoulated fields
    """
    # Query for user in the 'User' table
    user = User.objects.get(email=request.user.email)

    # Case 1: We have received a POST request with some data
    if request.method == 'POST':
        # Check to see if we are creating a new user information entry or updating an existing one
        if UserInformation.objects.filter(user=user).exists():
            form = UserInformationForm(request.POST, instance=UserInformation.objects.get(user=user))
        else:
            form = UserInformationForm(request.POST)

        # Case 1a: A valid user profile form
        if form.is_valid():
            # Since 'user' is a foreign key, we must store the queried entry from the 'User' table
            user_info = form.save(commit=False)
            user_info.user = user
            # user_info.user_class.add(Class.objects.get(class_name=form.cleaned_data['user_class']))
            user_info.save()

            request.session.set_expiry(0)
            return redirect("/accounts/profile")
        # Case 1b: Not a valid user profile form, render the settings page with the current form
        else:
            return render(request, "accounts/settings.html", {'form': form})
    # Case 2: We have received something other than a POST request
    else:
        # Case 2a: The user exists in our user information table.
        if UserInformation.objects.filter(user=user).exists():
            form = UserInformationForm(instance=UserInformation.objects.get(user=user),
                                       initial={'user_email': request.user.email})
        # Case 2b: The user email doesn't exist in our user information table.
        else:
            form = UserInformationForm(initial={'user_email': request.user.email, 'user_nickname': user.first_name})

        request.session.set_expiry(0)
        return render(request, "accounts/settings.html", {'form': form})
