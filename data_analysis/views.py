"""
This module contains our Django views for the "data_analysis" application.
"""

# Create your views here.
from django.shortcuts import render, redirect
from tutor.py_helper_functions.tutor_helper import user_auth_inst, lesson_set_auth


def instructor(request):
    """function instructor This function handles the view for the instructor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    # get all lesson sets, display
    if request.method == 'POST':
        # Will this include where the data is updated? Such as selecting different visuals to interact with?
        if user_auth_inst(request):
            # Take instructor to data view
            if lesson_set_auth(request):
                return redirect("/tutor/tutor")
            else:
                return redirect("accounts:profile")
        else:
            return redirect("/accounts/settings")
    else:

        return render(request, "data_analysis/visual.html")
