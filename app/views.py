from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, "app/homePage.html")


def tutor(request):
    if request.user.is_authenticated:
        return render(request, "app/lesson_template.html")
    else:
        return render(request, "accounts/login.html")
