"""
This module contains our Django views for the "tutor" application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Lesson, LessonSet
from accounts.models import UserInformation
import json
from django.http import JsonResponse


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
                    if current_user.current_lesson_index >= len(current_user.current_lesson_set.lessons.all()):
                        print("10")
                        return redirect("accounts:profile")
                    print("11")
                    return redirect("/tutor/tutor")
            else:
                return redirect("/accounts/settings")
        else:
            return redirect("/accounts/login")
    else:
        print("calling catalog")
        return render(request, "tutor/catalog.html", {'LessonSet': LessonSet.objects.all()})


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
        submitted_json = json.loads(request.body)
        # hook up websocket and verify
        # if success, return next lesson
        # if fail, do something

        '''
        This is a temporary FAKED verifer
        '''
        user = User.objects.get(email=request.user.email)
        # Case 2a: if the user exists
        if UserInformation.objects.filter(user=user).exists():
            current_user = UserInformation.objects.get(user=user)
            current_set = current_user.current_lesson_set.lessons.all()
            # Case 2aa: if the user has a current set
            if current_set.exists():
                if current_user.current_lesson_index < len(current_set) - 1:
                    # increase index of lesson set
                    current_user.current_lesson_index = current_user.current_lesson_index + 1
                    current_user.save()
                    print("in 1")
                    return JsonResponse({'status': 'success'})
                else:
                    # Do something more here
                    print("in 2")
                    return redirect("/tutor/catalog")
            else:
                # Do something more here
                print("in 3")
                return redirect("accounts:profile")
        else:
            # Do something more here
            print("in 4")
            return redirect("accounts:profile")
    elif request.method == 'GET':
        # Ensure user exists
        user = User.objects.get(email=request.user.email)
        # Case 2a: if the user exists
        if UserInformation.objects.filter(user=user).exists():
            current_user = UserInformation.objects.get(user=user)
            current_set = current_user.current_lesson_set.lessons.all()
            # Case 2aa: if the user has a current set
            if current_set.exists():
                # Case 2aaa: if the current set has a lesson of index that the user is on, set to current lesson
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
                        print(current_lesson.instruction)
                        print(current_lesson)
                        return render(request, "tutor/tutor.html",
                                      {'lessonName': current_lesson.lesson_title,
                                       'concept': current_lesson.lesson_concept.all(),
                                       'instruction': current_lesson.instruction,
                                       'code': current_lesson.code.lesson_code,
                                       'referenceSet': current_lesson.reference_set.all(),
                                       'reason': current_lesson.reason.reasoning_question,
                                       'reason_type': current_lesson.reason.reasoning_type,
                                       'screen_record': current_lesson.screen_record})
                    else:
                        # Do something more here
                        return redirect("accounts:profile")
                # Case 2aab: if the current lesson doesnt exist, this would mean set could be complete
                else:
                    # Do something more here
                    return redirect("accounts:profile")
                    # Case 2aab: if the current lesson doesnt exist, this would mean set could be complete
            # Case 2ab: the user does not have a current set, send them to get one
            else:
                return redirect("accounts:profile")
        # Case 2b: if the user doesnt exist, redirect to settings
        else:
            return redirect("accounts:profile")

    # might want an if get for next lesson/ load lesson
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
                if current_user.current_lesson_index < len(current_set):
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
                        return redirect("tutor:catalog")
                else:
                    print("5")
                    return redirect("tutor:catalog")
            # Case 2ab: the user does not have a current set, send them to get one
            else:
                print("6")
                return redirect("tutor:catalog")
        # Case 2b: if the user doesnt exist, redirect to settings
        else:
            print("7")
            return redirect("tutor:catalog")
