"""
This module contains our Django views for the "tutor" application.
"""
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from core.models import Lesson, LessonSet, MainSet
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data, get_log_data, finished_lesson_count
from tutor.py_helper_functions.tutor_helper import user_auth, lesson_set_auth, check_feedback, not_complete, log_lesson, \
    check_type, alternate_lesson_check
from tutor.py_helper_functions.mutation import reverse_mutate, can_mutate


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

        if user_auth(request):
            # search for lesson set
            if lesson_set_auth(request):
                return redirect("/tutor/tutor")
            else:
                print("lesson set auth returned false")
                return redirect("accounts:profile")
        else:
            return redirect("/accounts/settings")
    else:
        return render(request, "tutor/catalog.html", {'LessonSet': MainSet.objects.all()})


@login_required(login_url='/accounts/login/')
def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """

    print(request)

    # Case 1: We have received a POST request submitting code (needs a lot of work)
    if request.method == 'POST':
        # Case 1a: if the user exists
        if user_auth(request):
            # submitted_json = json.loads(request.body.decode('utf-8'))
            # if success, return next lesson
            # if fail, do something
            # Case 1aa: if the user has not completed set

            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            current_lesson = Lesson.objects.get(lesson_name=current_user.current_lesson_name)

            status = json.loads(request.body.decode('utf-8'))['status']
            print("status: ", status)
            submitted_answer = json.loads(request.body.decode('utf-8'))['answer'].replace(" ", "")

            submitted_answer = reverse_mutate(submitted_answer)

            log_data(request)

            if status == "success":
                log_lesson(request)
                main_set = MainSet.objects.filter(set_name=current_user.current_main_set)[0]
                print(main_set)

                # if they are correct in a alt lesson, find correct to send to
                if current_lesson.is_alternate and current_user.current_lesson_index != 0:
                    print(current_lesson.correct, "%%%%%%%%%%")
                    current_user.current_lesson_name = Lesson.objects.get(lesson_name=current_lesson.correct).lesson_name
                    index = 0
                    for index, item in enumerate(current_user.current_lesson_set.lessons.all()):
                        print(index, "&&&&&&&&&", item.lesson_name)
                        if item.lesson_name == current_lesson.correct:
                            break
                    current_user.current_lesson_index = index
                    current_user.save()
                    return JsonResponse(check_feedback(current_lesson, submitted_answer, status))

                # find the index of the next lesson set by enumerating query set of all sets
                for index, item in enumerate(main_set.lessons.all()):
                    if item == current_user.current_lesson_set:
                        break
                # return if last set to go through
                if index + 1 >= len(main_set.lessons.all()):
                    current_user.completed_sets = current_user.current_main_set
                    current_user.current_lesson_set = None
                    current_user.current_main_set = None
                    current_user.save()
                    print("in done: ", current_user.current_lesson_set)
                    return JsonResponse(check_feedback(current_lesson, submitted_answer, status))

                next_set = LessonSet.objects.get(set_name=main_set.lessons.all()[index+1])
                current_user.current_lesson_set = next_set
                current_user.current_lesson_name = next_set.first_in_set.lesson_name
                current_user.save()
            # if a user is not successful and there are alternates available
            print(current_lesson.sub_lessons_available, "%%%%%%%%%%")
            if status != "success" and current_lesson.sub_lessons_available:
                lesson_type = check_type(current_lesson, submitted_answer, status)
                alt_lesson = alternate_lesson_check(current_lesson, lesson_type)  # how to set this and render new page
                print(Lesson.objects.get(lesson_title=alt_lesson).lesson_name)
                current_user.current_lesson_name = Lesson.objects.get(lesson_title=alt_lesson).lesson_name
                for index, item in enumerate(current_user.current_lesson_set.lessons.all()):
                    if item == alt_lesson:
                        break
                current_user.current_lesson_index = index
                current_user.save()
                print("******* ", alt_lesson, " ", index)
            return JsonResponse(check_feedback(current_lesson, submitted_answer, status))

    # Case 2: We have received a GET request requesting code
    elif request.method == 'GET':
        # Ensure user exists
        # Case 2a: if the user exists
        print("in the get")
        if user_auth(request) and not_complete(request):

            # Case 2aa: if the user has a current set
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            current_set = current_user.current_lesson_set.lessons.all()
            set_len = len(current_user.current_main_set.lessons.all())
            print(set_len)
            num_done = finished_lesson_count(current_user)
            print("===============", num_done)
            # Case 2aaa: if the current set has a lesson of index that the user is on, set to current lesson
            if Lesson.objects.filter(lesson_title=current_set[current_user.current_lesson_index]).exists():
                current_lesson = Lesson.objects.get(lesson_title=current_set[current_user.current_lesson_index])
                print("in if 1")
                current_lesson.code.lesson_code = can_mutate(current_lesson)
                # create an ordered set
                ordered_set = current_user.current_main_set.lessons.all()
                index = 0
                for index, item in enumerate(current_user.current_main_set.lessons.all()):
                    if item == current_user.current_lesson_set:
                        break
                if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                    return render(request, "tutor/tutor.html",
                                  {'lesson': current_lesson,
                                   'lesson_code': current_lesson.code.lesson_code,
                                   'concept': current_lesson.lesson_concept.all(),
                                   'referenceSet': current_lesson.reference_set.all(),
                                   'reason': current_lesson.reason.reasoning_question,
                                   'mc_set': current_lesson.reason.mc_set.all(),
                                   'currLessonNum': current_user.current_lesson_index,
                                   'completedLessonNum': current_user.completed_lesson_index,
                                   'setLength': set_len,
                                   'finished_count': num_done,
                                   'orderedSet': ordered_set,
                                   'mood': current_user.mood,
                                   'review': 'none',
                                   'screen_record': current_lesson.screen_record,
                                   'audio_record': current_lesson.audio_record,
                                   'audio_transcribe': current_lesson.audio_transcribe,
                                   'user_email': request.user.email,
                                   'index': index})
                # Case 2aaab: if question is of type Text
                elif current_lesson.reason.reasoning_type == 'Text':
                    return render(request, "tutor/tutor.html",
                                  {'lesson': current_lesson,
                                   'lesson_code': current_lesson.code.lesson_code,
                                   'concept': current_lesson.lesson_concept.all(),
                                   'referenceSet': current_lesson.reference_set.all(),
                                   'reason': current_lesson.reason.reasoning_question,
                                   'currLessonNum': current_user.current_lesson_index,
                                   'completedLessonNum': current_user.completed_lesson_index,
                                   'setLength': set_len,
                                   'finished_count': num_done,
                                   'orderedSet': ordered_set,
                                   'mood': current_user.mood,
                                   'review': 'none',
                                   'screen_record': current_lesson.screen_record,
                                   'audio_record': current_lesson.audio_record,
                                   'audio_transcribe': current_lesson.audio_transcribe,
                                   'user_email': request.user.email,
                                   'index': index})
                # Case 2aaac: if question is of type none

                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'currLessonNum': current_user.current_lesson_index,
                               'completedLessonNum': current_user.completed_lesson_index,
                               'setLength': set_len,
                               'finished_count': num_done,
                               'orderedSet': ordered_set,
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': index})
    return redirect("accounts:profile")


@login_required(login_url='/accounts/login/')
def completed(request, index):
    """function previous This function handles retrieving the prev lesson.
        Args:
            request (HTTPRequest): A http request object created automatically by Django.
            index (int): The index of the lesson to retrieve
        Returns:
            HttpResponse: A generated http response object to the request depending on whether or not
                          the user is authenticated.
        """
    if request.method == 'GET':
        if user_auth(request):
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            if not_complete(request):
                main_set = MainSet.objects.filter(set_name=current_user.current_main_set)[0]

            item = main_set.lessons.all()[0]
            for count, item in enumerate(main_set.lessons.all()):
                if count == index:
                    break

            current_lesson = Lesson.objects.get(lesson_title=item.first_in_set)

            set_len = len(current_user.current_main_set.lessons.all())
            print("set len: ", set_len)
            num_done = finished_lesson_count(current_user)

            # create an ordered set
            ordered_set = current_user.current_main_set.lessons.all()
            count2 = 0
            for count2, item in enumerate(current_user.current_main_set.lessons.all()):
                if item == current_user.current_lesson_set:
                    break

            if index <= count2:
                lesson_info = get_log_data(current_user, index)
                print("lesson info: ", index)
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'lesson_code': lesson_info[0],
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'currLessonNum': current_user.current_lesson_index,
                               'setLength': set_len,
                               'finished_count': num_done,
                               'orderedSet': ordered_set,
                               'mood': lesson_info[1],
                               'past': lesson_info[2],
                               'completedLessonNum': count2,
                               'review': current_lesson.correct_feedback,
                               'index': index})
            return redirect("tutor:tutor")

    return redirect("accounts:profile")
