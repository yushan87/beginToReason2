"""
This module contains our Django views for the "tutor" application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Lesson, LessonSet
from accounts.models import UserInformation


def catalog(request):
    """function catalog This function handles the view for the catalog page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # get all lesson sets, display
    if request.method == 'POST':
        if request.user.is_authenticated:
            # set current lesson set for user with request.POST.get("set_name")
            user = User.objects.get(email=request.user.email)
            if UserInformation.objects.filter(user=user).exists():
                current_user = UserInformation.objects.get(user=user)
                # search for lesson set
                if LessonSet.objects.filter(set_name=request.POST.get("set_name")).exists():
                    current_set = LessonSet.objects.get(set_name=request.POST.get("set_name"))
                    current_user.current_lesson_set = current_set
                    current_user.save()
                    return redirect("/tutor/tutor")
            else:
                return redirect("/accounts/settings")
        else:
            return redirect("/accounts/login")
    return render(request, "tutor/catalog.html",
                  {'LessonSet': LessonSet.objects.all()})


@login_required(login_url='/accounts/login/')
def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # Case 1: We have received a POST request submitting code (needs a lot of work)
    if request.method == 'POST':
        print("\n\n\n\n********** in post **********\n\n\n\n")
        # hook up websocket and verify
        # if success, return next lesson
        # if fail, do something
        if Lesson.objects.filter(lesson_name='lesson2').exists():
            current_lesson = Lesson.objects.get(lesson_name='lesson2')
            return render(request, "tutor/tutor.html",
                          {'lessonName': current_lesson.lesson_title,
                           'concept': current_lesson.lesson_concept,
                           'instruction': current_lesson.instruction,
                           'code': current_lesson.code.lesson_code,
                           'referenceSet': current_lesson.reference_set.all(),
                           'reason': current_lesson.reason.reasoning_question})
        else:
            return render(request, "tutor/tutor.html")

    # Case 2: Load a current lesson for specific user
    else:
        # Ensure user exists
        user = User.objects.get(email=request.user.email)
        # Case 2a: if the user exists
        if UserInformation.objects.filter(user=user).exists():
            current_user = UserInformation.objects.get(user=user)
            current_set = current_user.current_lesson_set.lessons.all()
            # Case 2aa: if the user has a current set
            if current_set.exists():
                # Case 2aaa: if the current set has a lesson of index that the user is on, set to current lesson
                # need to add a check to make sure index is not out of range
                if Lesson.objects.filter(lesson_name=current_set[current_user.current_lesson_index]).exists():
                    current_lesson = Lesson.objects.get(lesson_name=current_set[current_user.current_lesson_index])
                    # Case 2aaaa: if the question is of type MC
                    if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                        return render(request, "tutor/tutor.html",
                                      {'lessonName': current_lesson.lesson_title,
                                       'concept': current_lesson.lesson_concept.all(),
                                       'instruction': current_lesson.instruction,
                                       'code': current_lesson.code.lesson_code,
                                       'referenceSet': current_lesson.reference_set.all(),
                                       'reason': current_lesson.reason.reasoning_question,
                                       'reason_type': current_lesson.reason.reasoning_type,
                                       'mc_set': current_lesson.reason.mc_set.all(),
                                       'screen_record': current_lesson.screen_record})
                    # Case 2aaab: if question is of type Text
                    elif current_lesson.reason.reasoning_type == 'Text':
                        return render(request, "tutor/tutor.html",
                                      {'lessonName': current_lesson.lesson_title,
                                       'concept': current_lesson.lesson_concept.all(),
                                       'instruction': current_lesson.instruction,
                                       'code': current_lesson.code.lesson_code,
                                       'referenceSet': current_lesson.reference_set.all(),
                                       'reason': current_lesson.reason.reasoning_question,
                                       'reason_type': current_lesson.reason.reasoning_type,
                                       'screen_record': current_lesson.screen_record})
                # Case 2aab: if the current lesson doesnt exist, this would mean set could be complete
                else:
                    # Do something more here
                    return render(request, "tutor/tutor.html")
            # Case 2ab: the user does not have a current set, send them to get one
            else:
                redirect("tutor/catalog")
        # Case 2b: if the user doesnt exist, redirect to settings
        else:
            return redirect("accounts/settings")
