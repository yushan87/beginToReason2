"""
This module contains our Django views for the "educator" application.
"""

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from educator.forms import ClassForm


@login_required(login_url='/accounts/login/')
def create_class(request):
    """function create_class This function handles the view for the create_class page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HTML Render of create class html
        form: a form for creating a new class
    """
    # get all lesson sets, display
    # Case 1: We have received a POST request with some data
    if request.method == 'POST':
        # Check to see if we are creating a new user information entry or updating an existing one
        form = ClassForm(request.POST)

        # Case 1a: A valid user profile form
        if form.is_valid():
            # Since 'user' is a foreign key, we must store the queried entry from the 'User' table
            new_class = form.save(commit=False)
            new_class.save()

            request.session.set_expiry(0)
            return redirect("/educator/instructor")
        # Case 1b: Not a valid user profile form, render the settings page with the current form
        else:
            return render(request, "educator/create_class.html", {'form': form})

    form = ClassForm()

    request.session.set_expiry(0)
    return render(request, "educator/create_class.html", {'form': form})


@login_required(login_url='/accounts/login/')
@csrf_protect
def instructor(request):
    """function create_class This function handles the view for the create_class page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    return render(request, "educator/instructor.html")
