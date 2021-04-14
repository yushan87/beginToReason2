"""
Main file for displaying graphs.
"""
import json
import re
from accounts.models import UserInformation
from core.models import LessonSet, MainSet
from data_analysis.models import DataLog
from data_analysis.py_helper_functions.graph_viewer.node import Node


# Takes a lesson index and returns a JSON representation fit for D3
def lesson_to_json(class_id, mainset_id, lessonset_index, is_anonymous):
    lesson_id = MainSet.objects.get(id=mainset_id).lessons.all()[lessonset_index].lessons.all()[0]
    (root, users) = _lesson_to_graph(class_id, lesson_id, is_anonymous)
    nodes = []
    edges = []
    allowed = _filter_by_appearances(root.return_family())
    for node in root.return_family():
        if allowed.get(node.get_hash_code()):
            nodes.append(node.to_dict())
            for edge in node.edge_dict():
                if allowed.get(edge["target"]):
                    edges.append(edge)
    return json.dumps({"nodes": nodes, "links": edges, "users": users})


# Returns JSON containing info that graph needs to display about the lesson
def lesson_info(mainset_id, lessonset_index):
    lesson_sets = MainSet.objects.get(id=mainset_id).lessons.all()
    lesson_set = lesson_sets[lessonset_index]
    lesson = lesson_set.lessons.all()[0]
    return json.dumps({"lessonName": lesson.lesson_name, "lessonTitle": lesson.lesson_title,
                       "lessonSetName": lesson_set.set_name, "code": lesson.code.lesson_code,
                       "prevLessonSet": _find_prev_lesson_set(lessonset_index),
                       "nextLessonSet": _find_next_lesson_set(lessonset_index, lesson_sets),
                       "confirms": _locate_confirm_indices(lesson.code.lesson_code)})


"""
Helper methods
"""


# Takes a lesson index and returns the START node of its graph representation
def _lesson_to_graph(class_id, lesson_id, is_anonymous):
    user_number = 1
    query = DataLog.objects.filter(lesson_key_id=lesson_id, class_key_id = class_id).order_by('user_key', 'time_stamp')
    users_dict = {}
    nodes_in_chain = []
    start_node = Node(Node.START_NAME, False)
    end_node = Node(Node.GAVE_UP_NAME, False)
    prev_node = start_node
    nodes_in_chain.append(prev_node)
    if not query:
        # Nobody has taken this lesson yet!
        return start_node, {}
    prev_student = query[0].user_key
    users_dict[str(user_number)] = _user_to_dict(prev_student, str(user_number), is_anonymous)
    for log in query:
        # Throw out instructors
        if is_user_instructor(log.user_key):
            continue
        # Only need confirm statements
        log.code = _locate_confirms(log.code)
        prev_node.add_appearance(str(user_number))
        # Is this kid same as the last one?
        if log.user_key != prev_student:
            # Nope!
            user_number += 1
            # Initialize new slot
            users_dict[str(user_number)] = _user_to_dict(log.user_key, str(user_number), is_anonymous)
            if not prev_node.is_correct:
                # Last kid gave up
                prev_node.add_next(end_node, str(user_number - 1))
                end_node.add_appearance(str(user_number - 1))
            else:
                # Last kid got it right
                chain_length = len(nodes_in_chain)
                for node in nodes_in_chain:
                    chain_length -= 1
                    node.add_distance(chain_length)
                    node.add_successful_appearance()
            prev_student = log.user_key
            nodes_in_chain.clear()
            prev_node = start_node
            nodes_in_chain.append(prev_node)
            start_node.add_appearance(str(user_number))
        # Runs every time
        users_dict.get(str(user_number))["attempts"] = users_dict.get(str(user_number)).get("attempts") + 1
        answer_correct = log.status == 'success'
        current_node = start_node.find_node(log.code)
        if not current_node:
            current_node = Node(log.code, answer_correct)
        prev_node.add_next(current_node, str(user_number))
        nodes_in_chain.append(current_node)
        prev_node = current_node
    # Post iteration
    prev_node.add_appearance(str(user_number))
    if not prev_node.is_correct:
        # Last kid gave up
        prev_node.add_next(end_node, str(user_number))
        end_node.add_appearance(str(user_number))
    else:
        # Last kid got it right
        chain_length = len(nodes_in_chain)
        for node in nodes_in_chain:
            chain_length -= 1
            node.add_distance(chain_length)
            node.add_successful_appearance()
    return start_node, users_dict


# Returns a dict containing the IDs of allowed nodes
def _filter_by_appearances(node_list):
    min_appearances = _find_optimal_min(node_list)
    allowed = {}
    for node in node_list:
        if (len(node.appearances) >= min_appearances) + (node.attempt == Node.GAVE_UP_NAME):
            allowed[node.get_hash_code()] = True
    return allowed


# Helper function, not used currently
def _find_optimal_min(node_list):
    appearances = []
    for node in node_list:
        appearances.append(len(node.appearances))
    appearances.sort()
    # 25 or less nodes will be allowed in graph
    max_nodes = 25
    if len(appearances) > max_nodes:
        return appearances[len(appearances) - max_nodes - 1] + 1
    # Just in case it's a teeny tiny lesson with a small amount of nodes
    return 0


# Returns the index of the previous lesson set
def _find_prev_lesson_set(current_lesson_set_index):
    if current_lesson_set_index == 0:
        # First lesson set in main set
        return -1

    return current_lesson_set_index - 1


# Returns index in the main set of the next lesson set
def _find_next_lesson_set(current_lesson_set_index, lesson_sets):
    if current_lesson_set_index + 1 == len(lesson_sets):
        # Last lesson in lesson set
        return -1

    return current_lesson_set_index + 1


def _user_to_dict(user, user_number, is_anonymous):
    if is_anonymous:
        return {"name": user_number, "attempts": 0, "gender": _get_user_info(user).user_gender}
    else:
        return {"name": _get_name(user), "attempts": 0, "gender": _get_user_info(user).user_gender}


def _get_name(user):
    if not user.first_name:
        return "admin"
    return user.first_name + " " + user.last_name


def _get_user_info(user):
    return UserInformation.objects.get(user=user.id)


def is_user_instructor(user_id):
    return _get_user_info(user_id).user_instructor


def _locate_confirms(code):
    lines = re.findall("Confirm [^;]*;|ensures [^;]*;", code)
    ans = ""
    for line in lines:
        ans += line[8:len(line) - 1]
        ans += ", "
    if len(lines) > 1:
        return "(" + ans[:len(ans) - 2] + ")"
    return ans[:len(ans) - 2]


def _locate_confirm_indices(code):
    confirms = []
    for index, line in enumerate(re.split("\\\\r\\\\n", code)):
        if re.search("Confirm [^;]*;|ensures [^;]*;", line):
            confirms.append(index)
    print(confirms)
    return confirms

