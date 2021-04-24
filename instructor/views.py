"""
This module contains our Django views for the "instructor" application.
"""
import random
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.models import UserInformation
from core.models import MainSet
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
                    # Get unique join code
                    join_code = random.randrange(100000, 999999, 1)

                    while True:
                        try:
                            Class.objects.get(join_code=join_code)
                            join_code = random.randrange(100000, 999999, 1)
                        except Class.DoesNotExist:
                            break

                    new_class = Class(class_name=class_name, join_code=join_code)
                    new_class.save()
                    new_relation = ClassMembership(user_id=current_user.id, class_taking_id=new_class.id, is_instructor=True)
                    new_relation.save()
                    messages.info(request, "Successfully created " + class_name + ". Students can input the code '" + str(join_code) + "' to join it.")
                return redirect("/instructor")
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
            return render(request, "instructor/assignments_instructor.html",
                          {'class': Class.objects.get(id=classID), 'main_sets': MainSet.objects.filter(show=True),
                           'today': date.today().isoformat()})
        else:
            # Case 1b: User doesn't teach class
            return redirect("/instructor/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")
