"""
This module contains our Django views for the "core" application.
"""
from accounts.models import UserInformation
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from educator.models import Class, ClassMembership
from educator.py_helper_functions.educator_helper import get_classes, user_in_class_auth
from tutor.py_helper_functions.tutor_helper import user_auth

User = get_user_model()


def home(request):
    """function home This function handles the view for the index page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "core/index.html")


@login_required(login_url='/accounts/login/')
def classes(request):
    """function classes This function handles the view for the classes page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if user_auth(request):
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        if request.method == 'POST':
            # Handle class join
            class_code = request.POST.get('class-code', None)
            if class_code is not None:
                try:
                    class_to_join = Class.objects.get(join_code=class_code)
                except Class.DoesNotExist:
                    class_to_join = None
                if class_to_join is not None:
                    if ClassMembership.objects.filter(user_id=current_user.id,
                                                      class_taking_id=class_to_join.id).exists():
                        messages.info(request, "You are already in " + str(class_to_join) + "!")
                    else:
                        new_relation = ClassMembership(user_id=current_user.id, class_taking_id=class_to_join.id,
                                                       is_educator=False)
                        new_relation.save()
                        messages.success(request, "Successfully added you to " + str(class_to_join))
                else:
                    messages.error(request, "Sorry, class code invalid!")
            else:
                messages.error(request, "Sorry, class code invalid!")
            return redirect("core:classes")
        return render(request, "core/classes.html", {'classes': get_classes(current_user)})
    else:
        return redirect("accounts:settings")


def class_view(request, classID):
    """function class_view This function handles the view for the class page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        classID (int): The ID of the class that's being viewed
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if user_auth(request):
        if user_in_class_auth(UserInformation.objects.get(user=User.objects.get(email=request.user.email)), classID):
            class_to_show = Class.objects.get(id=classID)
            return render(request, "core/student_assignments.html", {'class': class_to_show})
        else:
            return redirect("core:classes")
    else:
        return redirect("accounts:settings")


def privacy(request):
    """function login This function handles the view for the privacy page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "core/privacy.html")
