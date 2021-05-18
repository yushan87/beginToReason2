"""
This module contains model templates for the "instructor" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from datetime import date

from django.core.validators import MinLengthValidator
from django.db import models

from accounts.models import UserInformation
from core.models import MainSet, LessonSet, Lesson
import tutor.py_helper_functions as tutor_helper


class Class(models.Model):
    """
    A model of a class

    @param models.Model The base model
    """
    class_name = models.CharField("Name", max_length=100, validators=[MinLengthValidator(1)])  # Class name field
    join_code = models.CharField("Join_Code", max_length=6, validators=[MinLengthValidator(6)],
                                 unique=True)  # Code for joining class

    def __str__(self):
        """function __str__ is used to create a string representation of this class

        Returns:
            str: user email
        """
        return self.class_name

    def user_count(self):
        """function user_count is used to count how many students are in a class

        Returns:
            int: count of how many non-instructor users are enrolled
        """
        return ClassMembership.objects.filter(class_taking_id=self.id, is_instructor=False).count()

    def get_assignments(self):
        """function get_classes_taught This function gives assignments of a class

        Returns:
            List: List of assignments from a class
        """
        return Assignment.objects.filter(class_key_id=self.id).all()

    def get_current_assignments(self):
        """function get_classes_taught This function gives assignments of a class that are currently assigned

        Returns:
            List: List of assignments from a class
        """
        today = date.today()
        return Assignment.objects.filter(class_key_id=self.id, start_date__lte=today, end_date__gte=today).all()

    def get_future_assignments(self):
        """function get_classes_taught This function gives assignments of a class that haven't opened yet

        Returns:
            List: List of assignments from a class
        """
        return Assignment.objects.filter(class_key_id=self.id, start_date__gt=date.today()).all()

    def get_past_assignments(self):
        """function get_classes_taught This function gives assignments of a class that have closed already

        Returns:
            List: List of assignments from a class
        """
        return Assignment.objects.filter(class_key_id=self.id, end_date__lt=date.today()).all()

    def next_lesson_due_date(self):
        """function next_lesson_due_date handles finding the nearest due date of all lessons for a class

        Returns:
            Date: Date of nearest due assignment
        """
        record = date.max
        for assignment in self.get_current_assignments():
            if assignment.end_date < record:
                record = assignment.end_date

        if record == date.max:
            return None
        return record

    def get_students(self):
        """function get_students handles finding all non-instructor students in a class

        Returns:
            List: List of non-instructor students
        """
        membership_list = ClassMembership.objects.filter(class_taking=self, is_instructor=False)

        students_list = []
        for membership in membership_list:
            students_list.append(membership.user)

        return sorted(students_list, key=lambda x: x.user.last_login, reverse=True)

    def get_instructors(self):
        """function get_instructors handles finding all instructors of a class

        Returns:
            List: List of instructors
        """
        membership_list = ClassMembership.objects.filter(class_taking=self, is_instructor=True)

        instructors_list = []
        for membership in membership_list:
            instructors_list.append(membership.user)

        return sorted(instructors_list, key=lambda x: x.user.last_login, reverse=True)


class Assignment(models.Model):
    """
    A class-specific main set with a start and end date

    @param models.Model The base model
    """
    class_key = models.ForeignKey(Class, on_delete=models.CASCADE)  # Class this was assigned to
    main_set = models.ForeignKey(MainSet, on_delete=models.CASCADE)  # Main set assigned
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()

    def start_date_iso(self):
        """function start_date_iso formats start date for ISO for HTML

        Returns:
            String: Start date in YYYY-MM-DD ISO format
        """

        return self.start_date.isoformat()

    def end_date_iso(self):
        """function end_date_iso formats due date for ISO for HTML

        Returns:
            String: Due date in YYYY-MM-DD ISO format
        """

        return self.end_date.isoformat()

    def get_user_lesson(self, user_id):
        """function get_user_lesson a helper function to retrieve a user's current lesson set and lesson on an
        assignment

        Returns:
            current lesson set, current set index, current lesson, current lesson index, is_alternate (whether current
            lesson is an alternate or not)
        """
        if AssignmentProgress.objects.all().filter(assignment_key_id=self.id, user_info_key_id=user_id).exists():
            progress = AssignmentProgress.objects.all().get(assignment_key_id=self.id, user_info_key_id=user_id)
            if AlternateProgress.objects.all().filter(progress=progress).exists():
                # User is in an alt lesson
                alt_progress = AlternateProgress.objects.all().filter(progress=progress).order_by('-alternate_level')[0]
                return alt_progress.lesson_set, progress.current_set_index, \
                       alt_progress.lesson_set.lesson_by_index(alt_progress.current_lesson_index), \
                       alt_progress.current_lesson_index, True
            # User is not in an alt lesson
            progress = AssignmentProgress.objects.all().get(assignment_key_id=self.id, user_info_key_id=user_id)
            lesson_set = self.main_set.set_by_index(progress.current_set_index)
            return lesson_set, progress.current_set_index, lesson_set.lesson_by_index(progress.current_lesson_index), \
                   progress.current_lesson_index, False
        # Not in the assignment currently
        return None, -1, None, -1, False

    def advance_user(self, user_id):
        """function advance_user a helper function to move a user on to the next lesson
        Returns:
            if there's more to the assignment (false if complete, true if incomplete)
        """
        if AssignmentProgress.objects.all().filter(assignment_key_id=self.id, user_info_key_id=user_id).exists():
            progress = AssignmentProgress.objects.all().get(assignment_key_id=self.id, user_info_key_id=user_id)
            if AlternateProgress.objects.all().filter(progress=progress).exists():
                # User is in an alt lesson
                alt_progress = AlternateProgress.objects.all().filter(progress=progress).order_by('-alternate_level')[0]
                alt_progress.current_lesson_index += 1
                # Does the lesson set have a lesson for the incremented index?
                if alt_progress.lesson_set.lesson_by_index(alt_progress.current_lesson_index) is None:
                    # No! This means the alt lesson is complete and we can go up a level.
                    alt_progress.delete()
                else:
                    alt_progress.save()
                return True
            # User is not in an alt lesson but user is in the assignment
            progress.current_lesson_index += 1
            # Does the lesson set have a lesson for the incremented index?
            lesson_set = self.main_set.set_by_index(progress.current_set_index)
            if lesson_set.lesson_by_index(progress.current_lesson_index) is not None:
                # Yes!
                progress.save()
                return True
            # No! I need to increment the lesson set.
            progress.current_set_index += 1
            # Does the main set have a set for the incremented index?
            if self.main_set.set_by_index(progress.current_set_index) is not None:
                # Yes!
                progress.current_lesson_index = 0
                progress.save()
                return True
            progress.save()
            # No! The user has completed the assignment.
            return False
        # Not in the assignment currently
        return False

    def alternate_check(self, user_id, submitted_answer):
        """function advance_user a helper function to move a user to an alternate lesson. Call whenever a user gets
        a question wrong.
        """
        if not AssignmentProgress.objects.all().filter(assignment_key_id=self.id, user_info_key_id=user_id).exists():
            # Not in the assignment currently
            return

        progress = AssignmentProgress.objects.all().get(assignment_key_id=self.id, user_info_key_id=user_id)
        current_lesson = self.main_set.set_by_index(progress.current_set_index) \
            .lesson_by_index(progress.current_lesson_index)

        alt_lesson = tutor_helper.tutor_helper.alternate_lesson_check(current_lesson,
                                                                      tutor_helper.tutor_helper.check_type(
                                                                          current_lesson, submitted_answer))
        if alt_lesson is not None:
            print("I would have redirected to", alt_lesson)
            pass

        # check if we changed to an alternate
        if Lesson.objects.get(lesson_title=alt_lesson).lesson_name != current_user.current_lesson_name:
            unlock_next = True
            current_user.current_lesson_name = Lesson.objects.get(lesson_title=alt_lesson).lesson_name
            for index, item in enumerate(current_user.current_lesson_set.lessons.all()):
                if item == alt_lesson:
                    break
            current_user.current_lesson_index = index
            current_user.save()
            print("******* ", alt_lesson, " ", index)


class AssignmentProgress(models.Model):
    """
    A many-to-many between Assignment and UserInformation that stores progress on the assignment's main set

    @param models.Model The base model
    """
    assignment_key = models.ForeignKey(Assignment, on_delete=models.CASCADE)  # Assignment
    user_info_key = models.ForeignKey(UserInformation, on_delete=models.CASCADE)  # User
    current_set_index = models.IntegerField(default=0)
    current_lesson_index = models.IntegerField(default=0)


class AlternateProgress(models.Model):
    """
    A model that keeps track of the alternate lessons a student may trigger throughout an assignment

    @param models.Model The base model
    """
    progress = models.ForeignKey(AssignmentProgress, on_delete=models.PROTECT, null=True)
    lesson_set = models.ForeignKey(LessonSet, on_delete=models.CASCADE)
    current_lesson_index = models.IntegerField(default=0)
    alternate_level = models.IntegerField(default=0)  # How 'deep' it is - starts at 0 and as a user continues to
    # activate alternate lessons, makes more with larger levels


class ClassMembership(models.Model):
    """
    A many-to-many containing a boolean signifying whether user is instructor of class or not

    @param models.Model The base model
    """
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    class_taking = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
