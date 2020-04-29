from django.http import Http404
from django.shortcuts import render

from .models import Lesson
# Create your views here.

def index(request):
    return render(request, "app/index.html")

def lesson(request):
    try:
        lesson = Lesson.objects.get(pk=1)
    except Lesson.DoesNotExist:
        raise Http404("Lesson does not exist")
    return render(request, "app/lesson_template.html", {'Lesson':lesson,'content': "Lessons goes here!"})

def testPage(request):
    return render(request, "app/test.html")


def progress(request):
    return render(request, "app/progress.html")

