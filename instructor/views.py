"""
This module contains our Django views for the "instructor" application.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.models import UserInformation
from instructor.models import Class
from tutor.py_helper_functions.tutor_helper import user_auth
from instructor.py_helper_functions.instructor_helper import user_auth_inst, user_is_instructor, \
    get_classes, get_classes_taught


# Create your views here.


@login_required(login_url='/accounts/login/')
def instructor(request):
    """function instructor This function handles the view for the instructor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    # Is user valid?
    if user_auth(request):
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        # Case 1: User is valid
        # Is user instructor?
        if user_is_instructor(current_user):
            # Case 1a: User is instructor. Return class view
            return render(request, "instructor/instructor.html", {'classes': get_classes_taught(current_user)})
        else:
            # Case 1b: User doesn't exist in table
            return redirect("/accounts/settings")

    # Case 2: User not an instructor
    # Is user a user?
    elif user_auth(request):
        # Case 2a: User is user. Go to profile page
        return redirect("/accounts/profile")

    else:
        # Case 2b: User not user. Go to login
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def class_view(request, classID):
    """function instructor This function handles the view for the instructor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        classID (int): ID of the class requested

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    # Is user valid?
    if user_auth(request):
        # Case 1: User is valid
        user_info = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        # Does user instruct the class?
        if user_auth_inst(user_info, classID):
            # Case 1a: User is instructor of class
            return render(request, "instructor/mainsets.html", {'class': Class.objects.get(id=classID)})
        else:
            # Case 1b: User doesn't teach class
            return redirect("/instructor/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")
