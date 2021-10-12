from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import log_data, finished_lesson_count
from educator.models import Class, ClassMembership, Assignment
from educator.py_helper_functions.educator_helper import get_classes, user_in_class_auth, assignment_auth
from tutor.py_helper_functions.tutor_helper import user_auth, browser_response, replace_previous, send_to_verifier, \
    clean_variable
from tutor.py_helper_functions.mutation import can_mutate
from django.http import HttpResponse

import re
import math

User = get_user_model()

# Create your views here.
def parsons_problem(request, assignmentID):
    if request.method == 'GET':
        if assignment_auth(request, assignmentID):
            # Case 2a: User is valid and is taking this assignment
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=assignmentID)
            _, set_index, current_lesson, _, is_alternate = \
                assignment.get_user_lesson(current_user.id)
            num_done = finished_lesson_count(current_user)

            if not current_lesson.is_parsons:
                return redirect('tutor:tutor', assignmentID)

            # Just as we are altering the code here with mutate, this will pull the previous answer
            # to put in place for sub lessons. What identifiers do we need?

            current_lesson.code.lesson_code = can_mutate(current_lesson)
            current_lesson.code.lesson_code = replace_previous(current_user, current_lesson.code.lesson_code,
                                                               is_alternate)
            current_lesson.code.lesson_code = clean_variable(current_lesson.code.lesson_code)

            lessonCode = split_lesson_code(current_lesson)
            
            # Case 2aa: if questions if MC or Both
            if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                return render(request, 'parsons/parsons_problem.html',
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'lesson_code': lessonCode['set'],
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
                               'index': set_index,
                           'beginSetCode': lessonCode['beginSet'],
                           'endSetCode': lessonCode['endSet'],
                            'sortCode': lessonCode['sort'],
                            'comments': lessonCode['comments'],
                            'confirms': lessonCode['confirms'],
                               'multiConfirms': current_lesson.multi_confirms,
                               'isParsons': current_lesson.is_parsons})
            # Case 2ab: if question is of type Text
            elif current_lesson.reason.reasoning_type == 'Text':
                return render(request, 'parsons/parsons_problem.html',
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'lesson_code': lessonCode['set'],
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
                               'index': set_index,
                           'beginSetCode': lessonCode['beginSet'],
                           'endSetCode': lessonCode['endSet'],
                            'sortCode': lessonCode['sort'],
                            'comments': lessonCode['comments'],
                            'confirms': lessonCode['confirms'],
                               'multiConfirms': current_lesson.multi_confirms,
                               'isParsons': current_lesson.is_parsons})

            # Case 2ac: if question is of type none
            return render(request, 'parsons/parsons_problem.html',
                          {'lesson': current_lesson,
                           'assignment': assignment,
                           'lesson_code': lessonCode['set'],
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
                           'index': set_index,
                           'beginSetCode': lessonCode['beginSet'],
                           'endSetCode': lessonCode['endSet'],
                            'sortCode': lessonCode['sort'],
                            'comments': lessonCode['comments'],
                            'confirms': lessonCode['confirms'],
                            'multiConfirms': current_lesson.multi_confirms,
                               'isParsons': current_lesson.is_parsons})
    return redirect("accounts:profile")


def split_lesson_code(current_lesson):
    #Split code on newlines
    code = current_lesson.code.lesson_code.split(r'\n')
    sortableLines = current_lesson.sortable_lines.split(r'\n')

    firstCodeEndPointInd = 0
    finishedSetCode = False
    i = 0
    while i < len(code) and not finishedSetCode:
        #Get last line of code that is supposed to be set
        if 'Confirm' not in code[i]:
            if code[i] != r'\r':
                firstCodeEndPointInd = i
            
        else:
            finishedSetCode = True
        i += 1

    i = 0
    while i < len(code):
        #Find last confirm
        if 'Confirm' in code[i]:
            lastConfirm = i
        i += 1

    setCode = ""
    sortableCode = []
    confirms = []


    firstCodeEndPoint = current_lesson.code.lesson_code.find(code[firstCodeEndPointInd])
    beginSet = current_lesson.code.lesson_code[0:firstCodeEndPoint + len(code[firstCodeEndPointInd]) + 2]

    endPoint = current_lesson.code.lesson_code.find(code[lastConfirm])
    endSet = current_lesson.code.lesson_code[endPoint: len(current_lesson.code.lesson_code)]

    #Get sortable lines of code
    loopIndex = -1
    comments = []
    i = 0
    while i < len(sortableLines):
        if 'While' in sortableLines[i] or 'For' in sortableLines[i]:
            loopIndex += 1
            comments.append("")
        

        if 'increasing' in sortableLines[i] or 'decreasing' in sortableLines[i] or 'changing' in sortableLines[i]:
            sortableLines[i] = sortableLines[i].replace(r"\r", "")
            comments[loopIndex] += sortableLines[i].strip()

        
        elif sortableLines[i] != r'\r':
            #Get line of code with proper indentation
            sortableLines[i] = sortableLines[i].replace(r"\r", "")
            line = sortableLines[i].strip()
            numTabs = 0
            if len(sortableLines[i]) > len(line):
                numTabs = ((len(sortableLines[i]) - len(line)) - 8) / 4
            tabs = ""
            for _ in range(int(numTabs)):
                tabs += r'\t'
                
            sortableLines[i] = tabs + line
            if sortableLines[i] != "":
                sortableCode.append(sortableLines[i])
        i += 1
    
    #Combine and format set code for editor
    parsonsContainer = []

    setCode = beginSet
    setCode += r'\n'

    if not current_lesson.multi_confirms:
        for line in sortableCode:
            setCode += r'\n'
        

        numSortLines = len(sortableCode)
        numLines = 2 + math.ceil(float(2.5 * numSortLines)) + 1 - numSortLines
        for _ in range(numLines):
            setCode += r'\r\n'

        parsonsContainer.append(firstCodeEndPointInd * 3)
    
    else:
        
        i = firstCodeEndPointInd
        parsonsContainer.append(((i - 1) * 3) + 1)
        while i < len(code):
            if 'Confirm' in code[i] and 'Confirm' not in code[i - 1]:
                confirmInd = current_lesson.code.lesson_code.find(code[i])
                confirm = current_lesson.code.lesson_code[confirmInd: confirmInd + len(code[i])]
                confirm = confirm.replace(r'\r', "")
                confirms.append(confirm)

            i += 1
    
    setCode += endSet

    beginSet = beginSet.replace("    ", r"\t")
    endSet = endSet.replace("    ", r"\t")
    i = 0
    while i < len(confirms):
        confirms[i] = confirms[i].replace("    ", r"\t")
        i += 1

    lessonCode = {'beginSet': beginSet,
                  'endSet': endSet,
                  'set': setCode,
                'sort': sortableCode,
                'confirms': confirms,
                'comments': comments,}
    
    return lessonCode


def advanceParsonsLesson(request, assignmentID):
    if request.method == 'GET':
        if user_auth(request):
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=assignmentID)

            assignment.advance_user(current_user.id)

            return HttpResponse(status = 204)