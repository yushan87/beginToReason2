import json
from data_analysis.models import DataLog
from core.models import Lesson, LessonSet


# Returns JSON array of lessons in the set
def get_set_stats(lesson_set_id):
    lesson_set_list = []
    print("\n\n\n")
    print(LessonSet.objects.all())
    print("hihihi")
    print("\n\n\n")
    for lesson in LessonSet.objects.get(id=lesson_set_id).lessons:
        lesson_set_list.append(get_lesson_stats(lesson.id))
    return json.dumps(lesson_set_list)


# Returns a dict of a single lesson for lesson statistics
def get_lesson_stats(lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    lesson_dict = {{"name": lesson.lesson_name, "title": lesson.lesson_title}}
    lesson_dict.update(get_user_stats(lesson_id))
    return lesson_dict


# Returns a dictionary of the user-specific stats (e.g. avg. num of attempts)
def get_user_stats(lesson_id):
    query = DataLog.objects.filter(
        lesson_key_id=lesson_id).order_by('user_key', 'time_stamp')
    if not query[0]:
        return {"userCount": 0, "completionRate": 0, "firstTryRate": 0, "averageAttempts": 0}
    user_count = 1
    completions = 0
    attempts = 0
    first_try = int(query[0].status == 'correct')
    prev_student = query[0].user_key
    for log in query:
        if log.user_key != prev_student:
            # New student!
            user_count += 1
            prev_student = log.user_key
            first_try += int(log.status == 'success')
        completions += int(log.status == 'success')
        attempts += 1
    return {"userCount": user_count, "completionRate": completions / user_count, "firstTryRate": first_try / user_count, "averageAttempts": attempts / user_count}
