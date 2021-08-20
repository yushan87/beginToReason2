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

User = get_user_model()

# Create your views here.
def parsons_problem(request, current_lesson):
    #Split code on newlines
    current_lesson.code.lesson_code = current_lesson.code.lesson_code.replace('/*expression*/', current_lesson.correctExpression)
    code = current_lesson.code.lesson_code.split(r'\n')

    setCode = ""
    sortableCode = []

    #Read in lines that will just be displayed
    i = 0
    while 'Var' not in code[i]:
        i += 1

    beginPoint = current_lesson.code.lesson_code.find(code[i])
    beginSet = current_lesson.code.lesson_code[0:beginPoint + len(code[i]) + 2]

    #Get sortable lines of code
    i += 1
    while 'Confirm' not in code[i]:
        if code[i] != '\r':
            #Get line of code with proper indentation
            line = code[i].strip()
            numTabs = 0
            if len(code[i]) > len(line):
                numTabs = ((len(code[i]) - len(line)) - 9) / 4
            tabs = ""
            for _ in range(int(numTabs)):
                tabs += '\t'
                
            code[i] = tabs + line
            sortableCode.append(code[i])
        i += 1

    #Get rest of set code
    endPoint = current_lesson.code.lesson_code.find(code[i])
    endSet = current_lesson.code.lesson_code[endPoint: len(current_lesson.code.lesson_code)]
    
    #Combine and format set code for editor
    setCode = beginSet
    for _ in range(23):
        setCode += r'\r\n'
    setCode += endSet

    lessonCode = {'set': setCode, 
                'sort': sortableCode}
    
    return lessonCode