"""
This module contains our Django views for the "instructor" application.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.models import UserInformation
from instructor.models import Class
from tutor.py_helper_functions.tutor_helper import user_auth_inst, user_auth, user_in_class_auth


# Create your views here.


@login_required(login_url='/accounts/login/')
def instructor(request):
    """function instructor This function handles the view for the instructor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    # # get all lesson sets, display
    # if request.method == 'POST':
    #     # Will this include where the data is updated? Such as selecting different visuals to interact with?
    #     if user_auth_inst(request):
    #         # Take instructor to data view
    #         if lesson_set_auth(request):
    #             return redirect("/tutor/tutor")
    #         else:
    #             return redirect("accounts:profile")
    #     else:
    #         return redirect("/accounts/settings")
    # else:
    #     return render(request, "instructor/classView.html")

    # Is user an instructor?
    if user_auth_inst(request):
        # Case 1: User is instructor
        user = User.objects.get(email=request.user.email)
        # Does user exist in table?
        if user:
            # Case 1a: User is instructor and exists in user table. Return class view
            user_info = UserInformation.objects.get(user=user)
            return render(request, "instructor/instructor.html", {'classes': user_info.user_classes.all()})
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
    # Is user an instructor?
    if user_auth_inst(request):
        # Case 1: User is instructor
        user = User.objects.get(email=request.user.email)
        # Does user exist in table?
        if user:
            # Case 1a: User is instructor and exists in user table
            user_info = UserInformation.objects.get(user=user)
            # Does the instructor teach the class?
            if user_in_class_auth(user_info, classID):
                # Case 1aa: User does teach class
                return render(request, "instructor/sets.html", {'class': Class.objects.get(id=classID)})
            else:
                # Case 1ab: User doesn't teach class
                return redirect("/instructor/")
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
