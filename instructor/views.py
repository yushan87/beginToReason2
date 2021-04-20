"""
This module contains our Django views for the "instructor" application.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.models import UserInformation
from instructor.models import Class, ClassMembership
from tutor.py_helper_functions.tutor_helper import user_auth
from instructor.py_helper_functions.instructor_helper import user_auth_inst, user_is_instructor, get_classes_taught


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
            # Case 1a: User is instructor
            if request.method == 'POST':
                # Handle new class creation
                class_name = request.POST.get('class-name', None)
                if class_name is not None:
                    new_class = Class(class_name=class_name)
                    new_class.save()
                    new_relation = ClassMembership(user_id=current_user.id, class_taking_id=new_class.id, is_instructor=True)
                    new_relation.save()
            # Return class view
            return render(request, "instructor/instructor.html", {'classes': get_classes_taught(current_user)})
        else:
            # Case 1b: User doesn't exist in table
            return redirect("/accounts/settings")

    else:
        # Case 2: User not valid. Go to login
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def class_view_instructor(request, classID):
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
