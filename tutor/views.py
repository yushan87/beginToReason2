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
from instructor.py_helper_functions.instructor_helper import get_classes, user_in_class_auth, assignment_auth
from tutor.py_helper_functions.tutor_helper import user_auth, check_feedback, \
    check_type, alternate_lesson_check, replace_previous, send_to_verifier, overall_status
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
def grader(request):
    """function grader This function handles checking code sent by the JS.
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
            assignment = Assignment.objects.get(id=data['assignment'])
            current_lesson_set, set_index, current_lesson, lesson_index, is_alternate = assignment.get_user_lesson(current_user.id)
            print("lessons in set:", current_lesson_set.lessons())
            print("my lesson:", current_lesson)
            # Get submitted answer. No 'Confirm', no spaces, each ends w/ a semicolon
            submitted_answer = re.findall("Confirm [^;]*;|ensures [^;]*;", data['code'])
            submitted_answer = ''.join(submitted_answer)


            """
            REMEMBER TO LOG DATA
            """

            # Send it off to the RESOLVE verifier
            response, vcs = asyncio.run(send_to_verifier(data['code']))
            if response is not None:
                lines = overall_status(response, vcs)
                print("\n\n\nRESPONSE:", response)
                print("\n\nLINES:", lines)
                status = response['status']
            else:
                status = 'failure'
                lines = []
            """
            let lines = mergeVCsAndLineNums(vcs, lineNums.vcs)
            var
            confirmLine
            let
            vcLine = parseInt(lineNums.vcs[0].lineNum, 10)

            let
            currentAttemptAnswers = '';
            for (var i = 0; i < lines.lines.length; i++) {
            if (lines.lines[i].status == "success") {
            aceEditor.session.addGutterDecoration(lines.lines[i].lineNum-1, "ace_correct");
            confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace( / \s / g, '');
            confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace("Confirm", "");
            allAnswers = allAnswers + confirmLine  + "<br>";
            submitAnswers = submitAnswers + confirmLine;
            currentAttemptAnswers += confirmLine + '\n'
            }
            else {
            aceEditor.session.addGutterDecoration(lines.lines[i].lineNum-1, "ace_error");
            document.getElementById("answersCard").removeAttribute("hidden")
            confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace( / \s / g, '');
            confirmLine = aceEditor.session.getLine(lines.lines[i].lineNum-1).replace("Confirm", "");
            allAnswers = allAnswers + confirmLine  + "<br>";
            submitAnswers = submitAnswers + confirmLine;
            if (i == lines.lines.length - 1){
            allAnswers += "<br><br>";
            currentAttemptAnswers += confirmLine + '\n'
            }
            document.getElementById("pastAnswers").innerHTML = allAnswers;
            }
            }

            // posting
            back
            end
            data
            to
            log
            let
            data = {};
            data.name = name;
            data.answer = submitAnswers;
            data.allAnswers = allAnswers;
            data.code = code;
            if (hasFR){data.explanation = document.forms["usrform"]["comment"].value;}
            else if (hasMC){data.explanation = multiAnswer;}
            else {data.explanation = "No Explanation Requested";}

            const
            faces = document.querySelectorAll('input[name="smiley"]');
            let
            selectedValue;
            for (const x of faces) {
            if (x.checked) {
            selectedValue = x.value;
            data.face = selectedValue
            }
            }
            // The
            original
            post
            // $.postJSON("tutor", data, (results) = > {});
            submitAnswers = '';
"""
            if status == "success":
                # Update assignment progress
                has_next = assignment.advance_user(current_user.id)
                return JsonResponse(check_feedback(current_lesson, submitted_answer, status, True))
            else:
                # Activate alternate if needed
                assignment.alternate_check(current_user.id)
                return JsonResponse(check_feedback(current_lesson, submitted_answer, status, False))
    return redirect("accounts:profile")


def tutor(request, assignmentID, index=None):
    # View that returns a lesson's code (split from tutor.grader).
    if request.method == 'GET':
        if assignment_auth(request, assignmentID):
            # Case 2a: User is valid and is taking this assignment
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=assignmentID)
            current_set, set_index, current_lesson, lesson_index, is_alternate = \
                assignment.get_user_lesson(current_user.id)
            num_done = finished_lesson_count(current_user)
            print("===============", num_done)
            print("in if 1 - Current lesson: ", current_lesson)

            # Just as we are altering the code here with mutate, this will pull the previous answer
            # to put in place for sub lessons. What identifiers do we need?

            current_lesson.code.lesson_code = can_mutate(current_lesson)
            current_lesson.code.lesson_code = replace_previous(current_user, current_lesson.code.lesson_code,
                                                               is_alternate)

            # Case 2aa: if questions if MC or Both
            if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'reason': current_lesson.reason.reasoning_question,
                               'mc_set': current_lesson.reason.mc_set.all(),
                               'setLength': assignment.main_set.length(),
                               'finished_count': num_done,
                               'orderedSet': assignment.main_set.sets(),
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': set_index})
            # Case 2ab: if question is of type Text
            elif current_lesson.reason.reasoning_type == 'Text':
                return render(request, "tutor/tutor.html",
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'lesson_code': current_lesson.code.lesson_code,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set.all(),
                               'reason': current_lesson.reason.reasoning_question,
                               'setLength': assignment.main_set.length(),
                               'finished_count': num_done,
                               'orderedSet': assignment.main_set.sets(),
                               'mood': current_user.mood,
                               'review': 'none',
                               'screen_record': current_lesson.screen_record,
                               'audio_record': current_lesson.audio_record,
                               'audio_transcribe': current_lesson.audio_transcribe,
                               'user_email': request.user.email,
                               'index': set_index})

            # Case 2ac: if question is of type none
            return render(request, "tutor/tutor.html",
                          {'lesson': current_lesson,
                           'assignment': assignment,
                           'lesson_code': current_lesson.code.lesson_code,
                           'concept': current_lesson.lesson_concept.all(),
                           'referenceSet': current_lesson.reference_set.all(),
                           'setLength': assignment.main_set.length(),
                           'finished_count': num_done,
                           'orderedSet': assignment.main_set.sets(),
                           'mood': current_user.mood,
                           'review': 'none',
                           'screen_record': current_lesson.screen_record,
                           'audio_record': current_lesson.audio_record,
                           'audio_transcribe': current_lesson.audio_transcribe,
                           'user_email': request.user.email,
                           'index': set_index})
    return redirect("accounts:profile")
