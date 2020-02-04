from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "app/index.html")

def lesson(request):
    return render(request, "app/lesson_template.html", {'content': "Lessons goes here!"})

def testPage(request):
    return render(request, "app/test.html")