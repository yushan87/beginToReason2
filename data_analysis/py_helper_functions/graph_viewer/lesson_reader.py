"""
Main file for displaying graphs.
"""
import json
import re

from accounts.models import UserInformation
from data_analysis.models import DataLog
from data_analysis.py_helper_functions.graph_viewer.node import Node
from educator.models import Assignment # Takes a lesson index and returns a JSON representation fit for D3


def lesson_to_json(assignment_id, lesson_set_index, lesson_index, is_anonymous):
    assignment = Assignment.objects.get(id=assignment_id)
    lesson_set = assignment.main_set.set_by_index(lesson_set_index)
    lesson = lesson_set.lesson_by_index(lesson_index)
    (root, users) = _lesson_to_graph(assignment, lesson_set, lesson, is_anonymous)
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
def lesson_info(assignment_id, lesson_set_index, lesson_index):
    lesson_sets = Assignment.objects.get(id=assignment_id).main_set.sets()
    lesson_set = lesson_sets[lesson_set_index]
    lesson = lesson_set.lesson_by_index(lesson_index)
    return json.dumps({"lessonName": lesson.lesson_name, "lessonTitle": lesson.lesson_title,
                       "lessonSetName": lesson_set.set_name, "code": lesson.code.lesson_code,
                       "prevLesson": _find_prev_lesson(lesson_sets, lesson_set_index, lesson_index),
                       "nextLesson": _find_next_lesson(lesson_sets, lesson_set_index, lesson_index),
                       "confirms": _locate_confirm_indices(lesson.code.lesson_code)})


"""
Helper methods
"""


# Takes a lesson index and returns the START node of its graph representation
def _lesson_to_graph(assignment, lesson_set, lesson, is_anonymous):
    user_number = 0
    query = DataLog.objects.filter(assignment_key=assignment, lesson_set_key=lesson_set, lesson_key=lesson)\
        .order_by('user_key', 'time_stamp')
    start_node = Node(Node.START_NAME, False)
    if not query:
        # Nobody has taken this lesson yet!
        return start_node, {}
    users_dict = {}
    nodes_in_chain = []
    end_node = Node(Node.GAVE_UP_NAME, False)
    prev_node = start_node
    nodes_in_chain.append(start_node)
    prev_student = -1
    for log in query:
        # Throw out educators
        if is_user_educator(log.user_key):
            continue
        # Only need confirm statements
        log.code = _locate_confirms(log.code)
        # Is this kid same as the last one?
        if log.user_key != prev_student:
            # Nope!
            user_number += 1
            # Initialize new slot
            users_dict[str(user_number)] = _user_to_dict(log.user_key, str(user_number), is_anonymous)
            if prev_node != start_node:
                # Last kid gave up
                prev_node.add_next(end_node, str(user_number - 1))
                end_node.add_appearance(str(user_number - 1))
                nodes_in_chain.clear()
                nodes_in_chain.append(start_node)
                prev_node = start_node
            # Else last kid got it right, which was handled when they did get it right
            prev_student = log.user_key
            start_node.add_appearance(str(user_number))
        # Runs every time
        users_dict.get(str(user_number))["attempts"] = users_dict.get(str(user_number)).get("attempts") + 1
        answer_correct = log.status == 'success'
        current_node = start_node.find_node(log.code, answer_correct)
        if not current_node:
            current_node = Node(log.code, answer_correct)
        prev_node.add_next(current_node, str(user_number))
        nodes_in_chain.append(current_node)
        current_node.add_appearance(str(user_number))
        if answer_correct:
            chain_length = len(nodes_in_chain)
            for node in nodes_in_chain:
                chain_length -= 1
                node.add_distance(chain_length)
                node.add_successful_appearance()
            nodes_in_chain.clear()
            current_node = start_node
            nodes_in_chain.append(current_node)
        prev_node = current_node
    # Post iteration
    if prev_node != start_node:
        # Last kid gave up
        prev_node.add_next(end_node, str(user_number))
        end_node.add_appearance(str(user_number))
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


# Returns the URL addon for getting the preceding lesson's info
def _find_prev_lesson(lesson_sets, lesson_set_index, lesson_index):
    if lesson_index == 0:
        # First lesson in set
        if lesson_set_index == 0:
            # First overall, no previous!
            return None
        else:
            # Can decrement set
            lesson_set_index -= 1
            # Set to last lesson of current set
            lesson_index = len(lesson_sets[lesson_set_index].lessons()) - 1
    else:
        # Can decrement lesson
        lesson_index -= 1

    return str(lesson_set_index) + '/' + str(lesson_index)


# Returns the URL addon for getting the next lesson's info
def _find_next_lesson(lesson_sets, lesson_set_index, lesson_index):
    # Can we increment lesson_index?
    if lesson_index < len(lesson_sets[lesson_set_index].lessons()) - 1:
        # Yes!
        lesson_index += 1
    else:
        # No, then can we increment lesson_set_index?
        if lesson_set_index < len(lesson_sets) - 1:
            # We can do that!
            lesson_set_index += 1
            # Set to first lesson
            lesson_index = 0
        else:
            # Last lesson overall
            return None

    return str(lesson_set_index) + '/' + str(lesson_index)


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


def is_user_educator(user_id):
    return _get_user_info(user_id).user_educator


def _locate_confirms(code):
    declaration = re.findall("Var [^:]*", code)[0]
    declaration = declaration[4:len(declaration)]
    variables = re.split(", ", declaration)
    lines = re.findall("Confirm [^;]*;|ensures [^;]*;", code)
    ans = ""
    for line in lines:
        ans += _unmutate(line[8:len(line) - 1], variables)
        ans += ", "
    if len(lines) > 1:
        return "(" + ans[:len(ans) - 2] + ")"
    return ans[:len(ans) - 2]


def _locate_confirm_indices(code):
    confirms = []
    for index, line in enumerate(re.split("\\\\r\\\\n", code)):
        if re.search("Confirm [^;]*;|ensures [^;]*;", line):
            confirms.append(index)
    return confirms


# Replaces any order of IJK with specific order IJK
def _unmutate(code, variables):
    for index, var in enumerate(variables):
        code = code.replace(var, chr(81 + index))
    return code.replace("Q", "I").replace("R", "J").replace("S", "K")
