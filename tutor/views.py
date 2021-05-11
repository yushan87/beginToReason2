"""
This module contains our Django views for the "tutor" application.
"""
import asyncio
import json
import re
from asgiref.sync import async_to_sync, sync_to_async

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from core.models import Lesson, LessonSet, MainSet
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data, get_log_data, finished_lesson_count
from instructor.models import Class, ClassMembership, AssignmentProgress, Assignment
from instructor.py_helper_functions.instructor_helper import get_classes, user_in_class_auth
from tutor.py_helper_functions.tutor_helper import user_auth, assignment_auth, check_feedback, \
    check_type, alternate_lesson_check, replace_previous, send_to_verifier
from tutor.py_helper_functions.mutation import reverse_mutate, can_mutate

User = get_user_model()


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
        print("Attempting to open the assignment: ", request.POST)
        return lesson_code(request)
    else:
        return render(request, "tutor/catalog.html", {'LessonSet': MainSet.objects.all()})


@login_required(login_url='/accounts/login/')
def classes(request):
    """function catalog This function handles the view for the classes page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if user_auth(request):
        current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
        if request.method == 'POST':
            # Handle class join
            class_code = request.POST.get('class-code', None)
            if class_code is not None:
                try:
                    class_to_join = Class.objects.get(join_code=class_code)
                except Class.DoesNotExist:
                    class_to_join = None
                if class_to_join is not None:
                    if ClassMembership.objects.filter(user_id=current_user.id,
                                                      class_taking_id=class_to_join.id).exists():
                        messages.error(request, "You are already in " + str(class_to_join) + "!")
                    else:
                        new_relation = ClassMembership(user_id=current_user.id, class_taking_id=class_to_join.id,
                                                       is_instructor=False)
                        new_relation.save()
                        messages.info(request, "Successfully added you to " + str(class_to_join))
                else:
                    messages.error(request, "Sorry, class code invalid!")
            else:
                messages.error(request, "Sorry, class code invalid!")
            return redirect("/tutor/classes")
        return render(request, "tutor/classes.html", {'classes': get_classes(current_user)})
    else:
        return redirect("/accounts/settings")


def class_view(request, classID):
    """function catalog This function handles the view for the class page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        classID (int): The ID of the class that's being viewed
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    if user_auth(request):
        if user_in_class_auth(UserInformation.objects.get(user=User.objects.get(email=request.user.email)), classID):
            class_to_show = Class.objects.get(id=classID)
            return render(request, "tutor/assignments_student.html",
                          {'class': class_to_show})
        else:
            return redirect("/tutor/classes")
    else:
        return redirect("/accounts/settings")


@login_required(login_url='/accounts/login/')
def tutor(request):
    """function tutor This function handles the view for the tutor page of the application.
    Args:
        request (HTTPRequest): A http request object created automatically by Django.
    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
        lesson: Lesson object
        lesson_code: string of code
        concept: list of concepts
        referenceSet: list of references
        reason: string of question to ask or null
        mc_set: multiple choice options or null
        currLessonNum: int of index
        completedLessonNum: int of index of last completed (this might be depreciated and can remove)
        setLength: int of size of set
        finished_count: int of lessons finished
        orderedSet: list of lessons in order (this might be depreciated and can remove)
        mood: string of mood of user
        review: ?
        screen_record: boolean of to screen record
        audio_record: boolean of to audio record
        audio_transcribe: boolean of to transcribe audio
        user_email: string of user email
        index: int of order in main set
    """

    print(request)

    # Case 1: We have received a POST request submitting code (needs a lot of work)
    if request.method == 'POST':
        # Case 1a: if the user exists
        if user_auth(request):
            # if success, return next lesson
            # if fail, do something

            data = json.loads(request.body.decode('utf-8'))
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            progress = AssignmentProgress.objects.get(assignment_key_id=data['assignment'],
                                                      user_info_key=current_user)
            current_lesson = progress.current_lesson_set.lessons.all()[progress.current_lesson_index]
            print("lessons in set:", progress.current_lesson_set.lessons.all())
            print("my lesson:", current_lesson)
            # Get submitted answer. No 'Confirm', no spaces, each ends w/ a semicolon
            submitted_answer = re.findall("Confirm [^;]*;|ensures [^;]*;", data['code'])
            submitted_answer = ''.join(submitted_answer)


            """
            REMEMBER TO LOG DATA
            """
            unlock_next = False

            # Send it off to the RESOLVE verifier
            response = asyncio.run(send_to_verifier(data['code']))

            if response['status'] == "success":
                main_set = progress.assignment_key.main_set
                # if they are correct in a alt lesson, find correct to send to
                print("current_lesson.is_alternate: ", current_lesson.is_alternate,
                      " current_user.current_lesson_index: ", current_user.current_lesson_index)
                if current_lesson.is_alternate and current_user.current_lesson_index != 0:
                    print(current_lesson.correct, "%%%%%%%%%%")
                    current_user.current_lesson_name = Lesson.objects.get(
                        lesson_name=current_lesson.correct).lesson_name
                    index = 0

                    current_set = Lesson.objects.get(lesson_name=current_user.current_lesson_name)
                    print("CURRENT LESSON NAME: ", current_set, " ***** ",
                          current_user.current_lesson_set.lessons.all())

                    if current_set in current_user.current_lesson_set.lessons.all():
                        print("PRINT LESSONS: ", current_user.current_lesson_set.lessons.all())

                        # if current_user.current_lesson_name in current_user.current_lesson_set.lessons.all():
                        for index, item in enumerate(current_user.current_lesson_set.lessons.all()):
                            print(index, "&&&&&&&&&", item.lesson_name)
                            if item.lesson_name == current_lesson.correct:
                                break
                        current_user.current_lesson_index = index
                    else:
                        for index, item in enumerate(main_set.lessons.all()):
                            if item == current_user.current_lesson_set:
                                break

                        next_set = LessonSet.objects.get(set_name=main_set.lessons.all()[index + 1])
                        print("***************** ", next_set)
                        current_user.current_lesson_set = next_set
                        current_user.current_lesson_name = next_set.first_in_set.lesson_name
                        current_user.current_lesson_index = 0

                    current_user.save()
                    unlock_next = True
                    return JsonResponse(check_feedback(current_lesson, submitted_answer, status, unlock_next))

                # find the index of the next lesson set by enumerating query set of all sets
                for index, item in enumerate(main_set.lessons.all()):
                    if item == current_user.current_lesson_set:
                        break
                # return if last set to go through
                print("|||||||", index, "|||||||", len(main_set.lessons.all()))
                if index + 1 >= len(main_set.lessons.all()):
                    current_user.completed_sets.add(current_user.current_main_set)
                    current_user.current_lesson_set = None
                    current_user.current_main_set = None
                    current_user.save()
                    unlock_next = True
                    print("in done: ", current_user.current_lesson_set)
                    return JsonResponse(check_feedback(current_lesson, submitted_answer, status, unlock_next))
                    # return render(request, "accounts:profile")

                next_set = LessonSet.objects.get(set_name=main_set.lessons.all()[index + 1])
                current_user.current_lesson_set = next_set
                current_user.current_lesson_name = next_set.first_in_set.lesson_name
                current_user.save()

            # if a user is not successful and there are alternates available
            print(current_lesson.sub_lessons_available, "%%%%%%%%%%")
            if status != "success" and current_lesson.sub_lessons_available:
                lesson_type = check_type(current_lesson, submitted_answer, status)
                alt_lesson = alternate_lesson_check(current_lesson, lesson_type)  # how to set this and render new page

                # check if we changed to an alternate
                if Lesson.objects.get(lesson_title=alt_lesson).lesson_name != current_user.current_lesson_name:
                    unlock_next = True
                    current_user.current_lesson_name = Lesson.objects.get(lesson_title=alt_lesson).lesson_name
                    for index, item in enumerate(current_user.current_lesson_set.lessons.all()):
                        if item == alt_lesson:
                            break
                    current_user.current_lesson_index = index
                    current_user.save()
                    print("******* ", alt_lesson, " ", index)
            return JsonResponse(check_feedback(current_lesson, submitted_answer, status, unlock_next))
    return redirect("accounts:profile")


def lesson_code(request):
    # Internal function that returns a lesson's code (split from tutor.tutor).
    if request.method == 'POST':
        print("getting lesson's code")

        if assignment_auth(request):
            # Case 2a: User is valid and is taking this assignment
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=request.POST.get("assignment_id"))
            current_set, current_lesson = assignment.get_user_lesson(current_user.id)
            num_done = finished_lesson_count(current_user)
            print("===============", num_done)
            print("in if 1 - Current lesson: ", current_lesson)

            # Just as we are altering the code here with mutate, this will pull the previous answer
            # to put in place for sub lessons. What identifiers do we need?

            current_lesson.code.lesson_code = can_mutate(current_lesson)
            current_lesson.code.lesson_code = replace_previous(current_user, current_lesson.code.lesson_code,
                                                               current_lesson.is_alternate)

            # Case 2aa: if questions if MC or Both
            if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'assignment': assignment.id,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'reason': current_lesson.reason.reasoning_question,
                               'mc_set': current_lesson.reason.mc_set.all(),
                               'setLength': current_set.length(),
                               'finished_count': num_done,
                               'orderedSet': progress.assignment_key.main_set.lessons.all(),
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': index})
            # Case 2ab: if question is of type Text
            elif current_lesson.reason.reasoning_type == 'Text':
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'assignment': progress.assignment_key,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'reason': current_lesson.reason.reasoning_question,
                               'currLessonNum': progress.current_lesson_index,
                               'completedLessonNum': progress.completed_lesson_index,
                               'setLength': set_len,
                               'finished_count': num_done,
                               'orderedSet': progress.assignment_key.main_set.all(),
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': index})

            # Case 2ac: if question is of type none
            return render(request, "tutor/tutor.html",
                          {'lesson': current_lesson,
                           'assignment': progress.assignment_key,
                           'lesson_code': current_lesson.code.lesson_code,
                           'concept': current_lesson.lesson_concept.all(),
                           'referenceSet': current_lesson.reference_set.all(),
                           'currLessonNum': progress.current_lesson_index,
                           'completedLessonNum': progress.completed_lesson_index,
                           'setLength': set_len,
                           'finished_count': num_done,
                           'orderedSet': progress.assignment_key.main_set.lessons.all(),
                           'mood': current_user.mood,
                           'review': 'none',
                           'screen_record': current_lesson.screen_record,
                           'audio_record': current_lesson.audio_record,
                           'audio_transcribe': current_lesson.audio_transcribe,
                           'user_email': request.user.email,
                           'index': index})
    return redirect("accounts:profile")
