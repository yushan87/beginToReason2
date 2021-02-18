"""
This module contains our Django views for the "data_analysis" application.
"""

# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from core.models import Lesson, LessonSet, LessonIndex
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data, get_log_data, finished_lesson_count
from tutor.py_helper_functions.tutor_helper import user_auth, user_auth_inst, lesson_set_auth
from tutor.py_helper_functions.mutation import reverse_mutate, can_mutate


def instructor(request):
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

