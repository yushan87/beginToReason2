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
                               'sortCode': lessonCode['sort'],
                            'parsonsContainer': lessonCode['parsons']})
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
                               'sortCode': lessonCode['sort'],
                            'parsonsContainer': lessonCode['parsons']})

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
                            'sortCode': lessonCode['sort'],
                            'parsonsContainer': lessonCode['parsons']})
    return redirect("accounts:profile")


def split_lesson_code(current_lesson):
    print(current_lesson.code.lesson_code)
    #Split code on newlines
    code = current_lesson.code.lesson_code.split(r'\n')

    #Split list of correct assertions
    correctExpressions = current_lesson.correctExpression.split('; ')
    for i in range(len(correctExpressions)):
        if ';' not in correctExpressions[i]:
            correctExpressions[i] = correctExpressions[i] + ';'

        correctExpressions[i] = correctExpressions[i] + r'\n'

    firstCodeEndPointInd = 0
    finishedSetCode = False
    confirmInds = []
    lastConfirmInd = 0
    i = 0
    while i < len(code):
        #Get last line of code that is supposed to be set
        if not finishedSetCode:
            if 'Var' in code[i] or 'Read' in code[i] or 'Remember' in code[i] or (re.search(r'\d', code[i]) and ':=' in code[i]):
                firstCodeEndPointInd = i

        if 'If' in code[i] or 'While' in code[i]:
            finishedSetCode = True

        #Get last confirm statement
        if 'Confirm' in code[i]:
            lastConfirmInd = i

            confirmInds.append(i)

            #Get the last confirm statement for ech variable
            j = 0
            while j < len(confirmInds) - 1:
                if code[confirmInds[j]][16] == code[i][16]:
                    confirmInds.pop(0)

                j += 1

        i += 1

    setCode = ""
    sortableCode = []

    parsonsContainerPoint = firstCodeEndPointInd + 1 + 2
    parsonsContainerTop = 29
    i = 12

    if i < parsonsContainerPoint:
        while i < parsonsContainerPoint:
            parsonsContainerTop += 2
            i += 1
        #parsonsContainerTop += 1
    
    elif i > parsonsContainerPoint:
        while i > parsonsContainerPoint:
            parsonsContainerTop -= 2
            i -= 2
        parsonsContainerTop -= 1

    print(parsonsContainerTop)


    firstCodeEndPoint = current_lesson.code.lesson_code.find(code[firstCodeEndPointInd])
    beginSet = current_lesson.code.lesson_code[0:firstCodeEndPoint + len(code[firstCodeEndPointInd]) + 2]

    #Get sortable lines of code
    i = firstCodeEndPointInd + 1
    while i < lastConfirmInd:
        if code[i] != r'\r' and 'Confirm' not in code[i] and '--' not in code[i] and 'do' not in code[i]:
            #Get line of code with proper indentation
            line = code[i].strip()
            # print(code[i])
            # print(line)
            numTabs = 0
            if len(code[i]) > len(line):
                numTabs = ((len(code[i]) - len(line)) - 8) / 4
            tabs = ""
            for _ in range(int(numTabs)):
                tabs += r'\t'
                
            code[i] = tabs + line
            print(code[i])
            sortableCode.append(code[i])
        i += 1
    

    #Get rest of set code
    endPoint = current_lesson.code.lesson_code.rfind(code[lastConfirmInd + 2])
    endSet = current_lesson.code.lesson_code[endPoint: len(current_lesson.code.lesson_code)]

    print(endSet)
    
    #Combine and format set code for editor
    setCode = beginSet
    setCode += r'\n'
    for line in sortableCode:
        setCode += r'\t' + line
        setCode += r'\n'

    numSortLines = len(sortableCode)
    numLines = 2 + math.ceil(float(2.5 * numSortLines)) + 1 - numSortLines
    for _ in range(numLines):
        setCode += r'\r\n'

    j = 0
    k = 0
    while j < len(confirmInds):
        confirmPoint = current_lesson.code.lesson_code.rfind(code[confirmInds[j]])
        confirm = current_lesson.code.lesson_code[confirmPoint: confirmPoint + len(code[confirmInds[j]]) + 2]

        replacePoint = confirm.find('Confirm')
        replacePoint += 8
        confirm = confirm[:replacePoint] + correctExpressions[k]

        setCode += confirm

        j += 1
        k += 1
    
    setCode += endSet

    lessonCode = {'set': setCode, 
                'sort': sortableCode,
                'parsons': parsonsContainerTop}
    
    return lessonCode


def advanceParsonsLesson(request, assignmentID):
    if request.method == 'GET':
        if user_auth(request):
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=assignmentID)

            assignment.advance_user(current_user.id)

            return HttpResponse(status = 204)