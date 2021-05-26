import json
from data_analysis.models import DataLog
from core.models import MainSet
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import is_user_educator


# Returns stats for the mainset based around each lesson set
def get_set_stats(class_id, mainset_id):
    lesson_set_list = []
    for index, lesson_set in enumerate(MainSet.objects.get(id=mainset_id).lessons.all()):
        lesson_set_list.append(_get_lesson_set_stats(class_id, lesson_set, index))
    return json.dumps({"lessonSets": lesson_set_list, "statBounds": _find_stat_ranges(lesson_set_list)})


# Returns the main set's info (name, id)
def get_set_info(mainset_id):
    return {"name": MainSet.objects.get(id=mainset_id).set_name, "id": mainset_id}


"""
Helper Methods
"""


# Returns a dict of a single lesson set for main set statistics
def _get_lesson_set_stats(class_id, lesson_set, index):
    lesson_dict = {"name": lesson_set.set_name, "alternateCount": lesson_set.lessons.all().count() - 1}
    lesson_dict.update(_get_user_stats(class_id, lesson_set, index))
    return lesson_dict


# Returns a dictionary of the user-specific stats (e.g. avg. num of attempts)
def _get_user_stats(class_id, lesson_set, index):
    query = DataLog.objects.filter(lesson_set_key_id=lesson_set.id, class_key_id=class_id).order_by('user_key', 'time_stamp')
    if not query:
        # Means that no students have taken the lesson yet
        return {"userCount": 0, "completionRate": 0, "firstTryRate": 0, "averageAttempts": 0, "lessonSetIndex": index}
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
            "averageAttempts": attempts / user_count, "lessonSetIndex": index}


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
