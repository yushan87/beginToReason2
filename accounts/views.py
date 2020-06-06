from django.shortcuts import render, redirect
from .models import UserInformation
from . import forms
# Create your views here.


def login(request):
    return render(request, "accounts/login.html")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "accounts/profile.html")
    else:
        return render(request, "accounts/login.html")


def logout(request):
    return
