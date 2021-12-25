"""
This module contains our Django helper functions for the "educator" application.
"""
from accounts.models import UserInformation, User
from educator.models import ClassMembership, Class, Assignment, AssignmentProgress
import tutor.py_helper_functions.tutor_helper as tutor_helper


def user_is_educator(user_info):
    """function user_is_educator This function handles the auth logic for an educator

    Args:
        user_info: Model from accounts

    Returns:
        Boolean: A boolean to signal if the user instructs any class
    """
    return user_info.user_educator


def user_auth_inst(user_info, class_id):
    """function user_auth_inst This function handles the auth logic for an educator of a class

    Args:
        user_info: Model from accounts
        class_id (int): ID of the class in question

    Returns:
        Boolean: A boolean to signal if the user instructs class in question
    """
    membership = user_in_class_auth(user_info, class_id)
    if membership is not None:
        return membership.is_educator
    return False


def user_in_class_auth(user_info, class_id):
    """function user_in_class_auth This function handles the auth logic for users in classes

    Args:
        user_info: Model from accounts
        class_id (int): ID of the class in question

    Returns:
        ClassMembership: The relationship between the two, or None if doesn't exist
    """
    try:
        return ClassMembership.objects.get(user_id=user_info.id, class_taking=class_id)
    except ClassMembership.DoesNotExist:
        return None


def user_educates_class_auth(user_info, class_id):
    """function user_educates_class_auth This function handles the auth logic for whether a user has educator privileges
    over a class

    Args:
        user_info: Model from accounts
        class_id (int): ID of the class in question

    Returns:
        ClassMembership: The relationship between the two, or None if doesn't exist
    """
    try:
        return ClassMembership.objects.get(user_id=user_info.id, class_taking=class_id, is_educator=True)
    except ClassMembership.DoesNotExist:
        return None


def get_classes(user_info):
    """function get_classes This function gives classes a user is in

    Args:
        user_info: Model from accounts

    Returns:
        classes: List of classes the user is in
    """
    class_ids = []
    for membership in ClassMembership.objects.filter(user_id=user_info.id):
        class_ids.append(membership.class_taking_id)

    classes = []
    for class_id in class_ids:
        classes.append(Class.objects.get(id=class_id))

    return classes


def get_classes_taught(user_info):
    """function get_classes_taught This function gives classes a user teaches

    Args:
        user_info: Model from accounts

    Returns:
        classes: List of classes the user teaches
    """
    class_ids = []
    for membership in ClassMembership.objects.filter(user_id=user_info.id, is_educator=1):
        class_ids.append(membership.class_taking_id)

    classes = []
    for class_id in class_ids:
        classes.append(Class.objects.get(id=class_id))

    return classes


def assignment_auth(request, assignment_id=None):
    """function lesson_auth This function handles the auth logic for whether a student can take an assignment

    Args:
         request (HTTPRequest): A http request object created automatically by Django.
        assignment_id: An optional ID that can be input to check GET requests
    Returns:
        Boolean: A boolean to signal if the student is able to go into the assignment
    """
    if tutor_helper.user_auth(request):
        if assignment_id is None:
            assignment_id = request.POST.get("assignment_id")
        
        # Do we have the assignment in the DB?
        if Assignment.objects.filter(id=assignment_id).exists():
            assignment = Assignment.objects.get(id=assignment_id)
            current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))

            # Is the user already taking this assignment?
            if AssignmentProgress.objects.filter(assignment_key=assignment, user_info_key=current_user).exists():
                # Check that assignment hasn't been completed already
                current_lesson_set, _, current_lesson, _, _ = assignment.get_user_lesson(current_user.id)
                if current_lesson_set is None or current_lesson is None:
                    # Already completed
                    return False

                # Have a current lesson that is in progress
                return True
            else:
                # Is the user in the class for this assignment?
                if ClassMembership.objects.filter(user=current_user, class_taking=assignment.class_key).exists():
                    progress = AssignmentProgress(user_info_key=current_user, assignment_key=assignment)
                    progress.save()
                    
                    # Started new assignment
                    return True

                # User not in the class for this assignment!
                return False
        else:
            # Assignment doesn't exist!
            return False
    else:
        # Bad user!
        return False
