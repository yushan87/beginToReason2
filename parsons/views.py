import random

from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from accounts.models import UserInformation
from data_analysis.py_helper_functions.datalog_helper import finished_lesson_count
from educator.models import Assignment
from educator.py_helper_functions.educator_helper import assignment_auth
from tutor.py_helper_functions.tutor_helper import user_auth, replace_previous, clean_variable
from tutor.py_helper_functions.mutation import can_mutate

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

            lesson_code = split_lesson_code(current_lesson)            
            # Case 2aa: if questions if MC or Both
            if current_lesson.reason.reasoning_type == 'MC' or current_lesson.reason.reasoning_type == 'Both':
                return render(request, 'parsons/parsons_problem.html',
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set,
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
                               'beginSetCode': lesson_code['begin_set'],
                               'endSetCode': lesson_code['end_set'],
                               'sortCode': lesson_code['sort'],
                               'comments': lesson_code['comments'],
                               'confirms': lesson_code['confirms'],
                               'multiConfirms': current_lesson.multi_confirms,
                               'isParsons': current_lesson.is_parsons,
                               'hasDistractors': current_lesson.has_distractors})
            # Case 2ab: if question is of type Text
            elif current_lesson.reason.reasoning_type == 'Text':
                return render(request, 'parsons/parsons_problem.html',
                              {'lesson': current_lesson,
                               'assignment': assignment,
                               'concept': current_lesson.lesson_concept.all(),
                               'referenceSet': current_lesson.reference_set,
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
                               'beginSetCode': lesson_code['begin_set'],
                               'endSetCode': lesson_code['end_set'],
                               'sortCode': lesson_code['sort'],
                               'comments': lesson_code['comments'],
                               'confirms': lesson_code['confirms'],
                               'multiConfirms': current_lesson.multi_confirms,
                               'isParsons': current_lesson.is_parsons,
                               'hasDistractors': current_lesson.has_distractors})

            # Case 2ac: if question is of type none
            return render(request, 'parsons/parsons_problem.html',
                          {'lesson': current_lesson,
                           'assignment': assignment,
                           'concept': current_lesson.lesson_concept.all(),
                           'referenceSet': current_lesson.reference_set,
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
                           'beginSetCode': lesson_code['begin_set'],
                           'endSetCode': lesson_code['end_set'],
                           'sortCode': lesson_code['sort'],
                           'comments': lesson_code['comments'],
                           'confirms': lesson_code['confirms'],
                           'multiConfirms': current_lesson.multi_confirms,
                           'isParsons': current_lesson.is_parsons,
                           'hasDistractors': current_lesson.has_distractors})
    return redirect("accounts:profile")


def split_lesson_code(current_lesson):
    #Split code on newlines
    code = current_lesson.code.lesson_code.split(r'\n')
    sortables_lines = current_lesson.sortable_lines.split(r'\n')

    first_code_end_point_ind = 0
    finished_set_code = False
    i = 0
    while i < len(code) and not finished_set_code:
        #Get last line of code that is supposed to be set
        if 'Confirm' not in code[i] and 'end' not in code[i]:
            if code[i] != r'\r':
                first_code_end_point_ind = i
        else:
            finished_set_code = True
        i += 1

    i = 0
    while i < len(code):
        if not current_lesson.multi_confirms:
            #Find first confirm
            if 'Confirm' in code[i] or code[i].replace(r'\r', "").replace(r'\n', "").strip() == "end;":
                end_point_ind = i
                break
            i += 1
        else:
            #Find last confirm
            if 'Confirm' in code[i] or code[i].replace(r'\r', "").replace(r'\n', "").strip() == "end;":
                end_point_ind = i
            i += 1

    sortable_code = []
    confirms = []

    first_code_end_point = current_lesson.code.lesson_code.find(code[first_code_end_point_ind])
    begin_set = current_lesson.code.lesson_code[0:first_code_end_point + len(code[first_code_end_point_ind]) + 2]

    end_point = current_lesson.code.lesson_code.rfind(code[end_point_ind])
    end_set = current_lesson.code.lesson_code[end_point: end_point + len(current_lesson.code.lesson_code)]

    #Get sortable lines of code
    loop_index = -1
    comments = []
    i = 0
    while i < len(sortables_lines):
        if 'While' in sortables_lines[i] or 'For' in sortables_lines[i]:
            loop_index += 1
            comments.append("")
        
        if 'increasing' in sortables_lines[i] or 'decreasing' in sortables_lines[i] or 'changing' in sortables_lines[i]:
            sortables_lines[i] = sortables_lines[i].replace(r"\r", "")
            comments[loop_index] += sortables_lines[i].strip()

        
        elif sortables_lines[i] != r'\r':
            #Get line of code with proper indentation
            sortables_lines[i] = sortables_lines[i].replace(r"\r", "")
            line = sortables_lines[i].strip()
            num_tabs = 0
            if len(sortables_lines[i]) > len(line):
                num_tabs = ((len(sortables_lines[i]) - len(line)) - 8) / 4
            tabs = ""
            for _ in range(int(num_tabs)):
                tabs += r'\t'
                
            sortables_lines[i] = tabs + line
            if sortables_lines[i] != "":
                sortable_code.append(sortables_lines[i])
        i += 1
    
    confirm = ""
    if current_lesson.multi_confirms:
        i = first_code_end_point_ind + 1
        while i < end_point_ind:
            if len(code[i].replace(r'\r', "").replace(r'\n', "").strip()) != 0 and 'Confirm' not in code[i]:
                confirm_ind = current_lesson.code.lesson_code.find(code[i])
                confirm += current_lesson.code.lesson_code[confirm_ind: confirm_ind + len(code[i])]
                confirm += r"\n"

            if 'Confirm' in code[i]:
                confirm_ind = current_lesson.code.lesson_code.find(code[i])
                confirm += current_lesson.code.lesson_code[confirm_ind: confirm_ind + len(code[i])]

                if 'Confirm' in code[i + 1] and i + 1 != end_point_ind:
                    confirm_ind = current_lesson.code.lesson_code.find(code[i + 1])
                    confirm += r"\n"
                    confirm += current_lesson.code.lesson_code[confirm_ind: confirm_ind + len(code[i + 1])]
                    i += 1

                elif len(code[i + 1].replace(r'\r', "").replace(r'\n', "").strip()) != 0 and i + 1 != end_point_ind:
                    confirm_ind = current_lesson.code.lesson_code.find(code[i + 1])
                    confirm += r"\n"
                    confirm += current_lesson.code.lesson_code[confirm_ind: 
                    confirm_ind + len(code[i + 1])]
                    confirm += r"\n"
                    i += 1
                    
                confirm = confirm.replace(r'\r', "")
                confirms.append(confirm)
                confirm = ""

            i += 1

    begin_set = begin_set.replace("    ", r"\t")
    end_set = end_set.replace("    ", r"\t")
    i = 0
    while i < len(confirms):
        confirms[i] = confirms[i].replace("    ", r"\t")
        i += 1

    if current_lesson.multi_confirms:
        random.shuffle(sortable_code)
    print(confirms)

    lesson_code = {'begin_set': begin_set,
                  'end_set': end_set,
                  'sort': sortable_code,
                  'confirms': confirms,
                  'comments': comments,}
    
    return lesson_code

def advance_parsons_lesson(request, assignmentID):
    if request.method == 'GET':
        if user_auth(request):
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))
            assignment = Assignment.objects.get(id=assignmentID)

            assignment.advance_user(current_user.id)

            return HttpResponse(status = 204)
