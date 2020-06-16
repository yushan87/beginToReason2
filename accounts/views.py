"""
This module contains our Django views for the "accounts" application.
"""
from django.shortcuts import render, get_object_or_404
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
            form = CreateUser(request.POST)
            if form.is_valid():
                form.save()
                return render(request, "accounts/settings.html")
        else:
            registered_users = UserInformation.objects.all()
            count = 0
            while count < len(registered_users):
                # print(len(registered_users))
                # print(registered_users[count])
                # print(" and ")
                # print(request.user.username)
                request_name = str(request.user.username)
                registered_name = str(registered_users[count])
                if registered_name == request_name:
                    # print("username matches")
                    return render(request, "accounts/settings.html")
                count += 1
            # print(registered_users[count])
            # print(UserInformation.objects.get(user_email=request.user.email))
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
