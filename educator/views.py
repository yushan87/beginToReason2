"""
This module contains our Django views for the "educator" application.
"""
import random

from accounts.models import UserInformation
from core.models import MainSet
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from educator.models import Class, ClassMembership, Assignment
from educator.py_helper_functions.educator_helper import user_auth_inst, user_is_educator, get_classes_taught
from tutor.py_helper_functions.tutor_helper import user_auth


# Create your views here.
User = get_user_model()


@login_required(login_url='/accounts/login/')
def educator(request):
    """function educator This function handles the view for the educator page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    # Is user valid?
    if user_auth(request):
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        # Case 1: User is valid
        # Is user educator?
        if user_is_educator(current_user):
            # Case 1a: User is educator
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
                    new_relation = ClassMembership(user_id=current_user.id, class_taking_id=new_class.id, is_educator=True)
                    new_relation.save()
                    messages.info(request, "Successfully created " + class_name + ". Students can input the code '"
                                  + str(join_code) + "' to join it.")
                return redirect("/educator")
            # Return class view
            return render(request, "educator/educator.html", {'classes': get_classes_taught(current_user)})
        else:
            # Case 1b: User doesn't exist in table
            return redirect("/accounts/settings")

    else:
        # Case 2: User not valid. Go to login
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def class_view_educator(request, classID):
    """function educator This function handles the view for the educator page of the application.

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
            # Case 1a: User is educator of class

            if request.method == 'POST':
                # Handle assignment creation
                main_set = request.POST.get('main_set', None)
                start_date = date.fromisoformat(request.POST.get('start_date', date.today().isoformat()))
                end_date = request.POST.get('end_date', None)

                # Basically a do: while(False) loop
                while True:
                    if main_set is None:
                        messages.error(request, "You must select a main set!")
                        break
                    if end_date is None:
                        messages.error(request, "You must supply a due date!")
                        break
                    end_date = date.fromisoformat(end_date)
                    if end_date < start_date:
                        messages.error(request, "Assignment must open before it closes!")
                        break
                    new_assignment = Assignment(class_key_id=classID, main_set_id=main_set,
                                                start_date=start_date, end_date=end_date)
                    new_assignment.save()
                    return redirect(reverse('educator:class-view', args=[classID]))

            # Error carried from POST endpoints
            if 'error' in request.session:
                error = request.session['error']
                del request.session['error']
                messages.error(request, error)

            return render(request, "educator/assignments_educator.html",
                          {'class': Class.objects.get(id=classID), 'main_sets': MainSet.objects.filter(show=True),
                           'today': date.today().isoformat()})
        else:
            # Case 1b: User doesn't teach class
            return redirect("/educator/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def members(request, classID):
    """function educator This function handles the view the members of a class

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
            # Case 1a: User is educator of class

            if request.method == 'POST':
                # Do something
                main_set = request.POST.get('main_set', None)
                start_date = date.fromisoformat(request.POST.get('start_date', date.today().isoformat()))
                end_date = request.POST.get('end_date', None)

                # Basically a do: while(False) loop
                while True:
                    if main_set is None:
                        messages.error(request, "You must select a main set!")
                        break
                    if end_date is None:
                        messages.error(request, "You must supply a due date!")
                        break
                    end_date = date.fromisoformat(end_date)
                    if end_date < start_date:
                        messages.error(request, "Assignment must open before it closes!")
                        break
                    new_assignment = Assignment(class_key_id=classID, main_set_id=main_set,
                                                start_date=start_date, end_date=end_date)
                    new_assignment.save()
                    return redirect(reverse('educator:class-view', args=[classID]))

            # Error carried from POST endpoints
            if 'error' in request.session:
                error = request.session['error']
                del request.session['error']
                messages.error(request, error)

            return render(request, "educator/members.html",
                          {'class': Class.objects.get(id=classID)})
        else:
            # Case 1b: User doesn't teach class
            return redirect("/educator/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def edit_assignment(request):
    """function educator This function handles the POST request for editing/deleting an assignment

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    if request.method != 'POST':
        return redirect("/educator/")

    # Get assignment
    try:
        assignment_id = request.POST.get('assignment_id', -1)
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        # Assignment doesn't exist!
        return redirect('/educator/')

    # Is user valid?
    if user_auth(request):
        # Case 1: User is valid
        user_info = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        # Does user instruct the class?
        if user_auth_inst(user_info, assignment.class_key):
            # Case 1a: User is educator of class
            # Handle assignment edit
            delete = request.POST.get('delete_assignment', False)
            end_date = request.POST.get('end_date', None)

            # Basically a do: while(False) loop
            while True:
                if delete is not False:
                    # Delete the assignment
                    assignment.delete()
                    break
                if end_date is None:
                    request.session['error'] = "You must supply a due date!"
                    break
                end_date = date.fromisoformat(end_date)
                if end_date < assignment.start_date:
                    request.session['error'] = "Assignment must open before it closes!"
                    break
                assignment.end_date = end_date
                assignment.save()
                break

            return redirect(reverse('educator:class-view', args=[assignment.class_key_id]))
        else:
            # Case 1b: User doesn't teach class
            return redirect("/educator/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def edit_class(request):
    """function educator This function handles the POST request for renaming/deleting a class

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    if request.method != 'POST':
        return redirect("/educator/")

    # Get class
    try:
        class_id = request.POST.get('class_id', -1)
        class_to_edit = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        # Class doesn't exist!
        return redirect('/educator/')

    # Is user valid?
    if user_auth(request):
        # Case 1: User is valid
        user_info = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        # Does user instruct the class?
        if user_auth_inst(user_info, class_id):
            # Case 1a: User is educator of class
            # Handle class edit
            delete = request.POST.get('delete_class', False)
            new_name = request.POST.get('new_name', None)

            # Basically a do: while(False) loop
            while True:
                if delete is not False:
                    # Delete the class
                    class_to_edit.delete()
                    break
                if new_name is None:
                    request.session['error'] = "You must supply a class name!"
                    break
                class_to_edit.class_name = new_name
                class_to_edit.save()
                break

            return redirect(reverse('educator:main-view'))
        else:
            # Case 1b: User doesn't teach class
            return redirect("/educator/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def promote_student(request):
    """function educator This function handles the POST request for making a student an educator

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    if request.method != 'POST':
        return redirect("/educator/")

    # Get class
    try:
        class_id = request.POST.get('class_id', -1)
        Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        # Class doesn't exist!
        return redirect('/educator/')

    # Is user valid?
    if user_auth(request):
        # Case 1: User is valid
        user_info = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        # Does user instruct the class?
        if user_auth_inst(user_info, class_id):
            # Case 1a: User is educator of class
            # Handle promotion
            student_id = request.POST.get('student_id', None)

            # Basically a do: while(False) loop
            while True:
                if student_id is None:
                    request.session['error'] = "Server error. Try again?"
                    break

                try:
                    membership = ClassMembership.objects.get(user_id=student_id, class_taking_id=class_id)
                except ClassMembership.DoesNotExist:
                    request.session['error'] = "Server error. Try again?"
                    break

                try:
                    account = UserInformation.objects.get(id=student_id)
                except UserInformation.DoesNotExist:
                    request.session['error'] = "Server error. Try again?"
                    break

                account.user_educator = True
                membership.is_educator = True
                account.save()
                membership.save()
                break

            return redirect(reverse('educator:members', args=[class_id]))
        else:
            # Case 1b: User doesn't teach class
            return redirect("/educator/")
    else:
        # Case 2: User doesn't exist in table
        return redirect("/accounts/settings")
