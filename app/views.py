from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def home(request):
    return render(request, "app/homePage.html")

def tutor(request):
    return render(request, "app/lesson_template.html", {'content': "Lessons goes here!"})

def login(request):
    return render(request, "app/login.html")