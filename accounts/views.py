"""
This module contains our Django views for the "accounts" application.
"""
from django.shortcuts import render, redirect
from .models import UserInformation
from django.views.decorators.csrf import csrf_protect
from .forms import CreateUser


def login(request):
    """function login This function handles the view for the login page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    # if request.method == 'POST':
    # user = UserInformation(user_email=user.email, user_id=1234, user_name="test user")
    # user = UserInformation(request.POST)
    # user.save()
    # return redirect('accounts: profile')
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
        # print(request.user.email)
        if request.method == 'POST':
            #if UserInformation.getuser():
                # how to find user in db
                #a = UserInformation.getuser()
                #form = CreateUser(request.POST, instance=a)
                #form.save()
            #else:
                form = CreateUser(request.POST)
                # print(request.POST.get('user_name'))
                # print(request.POST.get('user_email'))
                # print(request.POST)

                # name = request.POST.get('user_name')
                # email = request.POST.get('user_email')

                # user = UserInformation(user_email=request.POST.get('user_email'), user_name=request.POST.get('user_name'))
                # user = CreateUser(email=email, name=name)
                form.save()
                return render(request, "accounts/settings.html")
        else:
            form = CreateUser(initial={'user_email': request.user.email, 'user_name': request.user.username})
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
