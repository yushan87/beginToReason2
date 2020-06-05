from django.shortcuts import render, redirect
from .models import UserInformation
from . import forms
# Create your views here.


def login(request):
    if request.method == 'POST':
        user = UserInformation(user_email="testemail@gmail.com", user_id=1234, user_name="test user")
        # user = UserInformation(request.POST)
        user.save()
        return redirect('accounts: profile') # have edit button redirect to some landing
    return render(request, "accounts/login.html")


def profile(request):
    return render(request, "accounts/profile.html")
