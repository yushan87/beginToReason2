import json

from data_analysis.models import DataLog
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import is_user_educator
from educator.models import Assignment, AssignmentProgress # Returns stats for the mainset based around each lesson set


def get_main_set_stats(assignment_id):
    main_set = Assignment.objects.get(id=assignment_id).main_set
    lesson_list = []
    for set_index, lesson_set in enumerate(main_set.sets()):
        for lesson_index, lesson in enumerate(lesson_set.lessons()):
            lesson_list.append(_get_lesson_stats(assignment_id, lesson_set, set_index, lesson, lesson_index))
    return json.dumps({"lessonSets": lesson_list, "statBounds": _find_stat_ranges(lesson_list)})


# Returns the main set's info (name, id)
def get_main_set_info(assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    return {"name": assignment.main_set.set_name, "id": assignment.main_set.id}


"""
Helper Methods
"""


# Returns a dict representing a single lesson for main set statistics
def _get_lesson_stats(assignment_id, lesson_set, set_index, lesson, lesson_index):
    lesson_dict = {"name": lesson_set.set_name, "set_index": set_index, "lesson_index": lesson_index}
    lesson_dict.update(_get_user_stats(assignment_id, lesson_set, lesson))
    lesson_dict.update(_count_current_users(assignment_id, set_index, lesson_index))
    return lesson_dict


# Returns a dictionary of the user-specific stats (e.g. avg. num of attempts)
def _get_user_stats(assignment_id, lesson_set, lesson):
    query = DataLog.objects.filter(assignment_key_id=assignment_id, lesson_set_key=lesson_set, lesson_key=lesson)\
        .order_by('user_key', 'time_stamp')
    if not query:
        # Means that no students have taken the lesson yet
        return {"userCount": 0, "completionRate": 0, "firstTryRate": 0, "averageAttempts": 0}
    user_count = 0
    completions = 0
    attempts = 0
    first_try = 0
    prev_log = None
    for log in query:
        # Throw out educators
        if is_user_educator(log.user_key):
            continue
        if not prev_log or log.user_key != prev_log.user_key:
            # New student!
            user_count += 1
            first_try += int(log.status == 'success')
            if prev_log:
                completions += int(prev_log.status == 'success')
        attempts += 1
        prev_log = log

    # Post iteration
    if prev_log:
        completions += int(prev_log.status == 'success')

    return {"userCount": user_count, "completionRate": completions / user_count, "firstTryRate": first_try / user_count,
            "averageAttempts": attempts / user_count}


def _count_current_users(assignment_id, set_index, lesson_index):
    count = AssignmentProgress.objects.filter(assignment_key_id=assignment_id, current_set_index=set_index,
                                              current_lesson_index=lesson_index).count()
    return {"currentUsers": count}


# Gets the ranges that outliers lie out of
def _find_stat_ranges(lesson_set_list):
    completion_rate = []
    first_try = []
    average_attempts = []
    length = 0
    for lesson in lesson_set_list:
        if not lesson.get("userCount"):
            continue
        length += 1
        completion_rate.append(lesson.get("completionRate"))
        first_try.append(lesson.get("firstTryRate"))
        average_attempts.append(lesson.get("averageAttempts"))
    return {"completionRate": _get_normal_range(completion_rate, length),
            "firstTryRate": _get_normal_range(first_try, length),
            "averageAttempts": _get_normal_range(average_attempts, length)}


# Currently returning just the quartiles because 1.5*IQR was too lenient
def _get_normal_range(data_list, list_length):
    if list_length < 2:
        return -1, 101
    data_list.sort()
    half_length = int(list_length / 2)
    if half_length % 2:
        # It's odd!
        quartile_1 = data_list[int(half_length / 2)]
        quartile_3 = data_list[list_length - int((half_length + 1) / 2)]
    else:
        # It's even!
        quartile_1 = (data_list[half_length / 2] + data_list[half_length / 2 - 1]) / 2
        quartile_3 = (data_list[list_length - half_length / 2] + data_list[list_length - half_length / 2 - 1]) / 2

    inter_quartile = quartile_3 - quartile_1
    return quartile_1, quartile_3
