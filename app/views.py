from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, "app/homePage.html")


def tutor(request):
    return render(request, "app/lesson_template.html", {'content': "Lessons goes here!"})
