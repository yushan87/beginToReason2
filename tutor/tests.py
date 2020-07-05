"""
This module contains our unit and functional tests for the "tutor" application.
"""
from django.test import TestCase

#from .models import Lesson, Reference


class LessonModelTests(TestCase):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    @staticmethod
    def test_add_multiple_references():
        """
        Ensure that lesson can contain multiple references


        l_1 = Lesson(lesson_name='Lesson1')
        l_1.save()
        l_2 = Lesson(lesson_name='Lesson2')
        l_2.save()
        l_3 = Lesson(lesson_name='Lesson3')
        l_3.save()

        r_1 = Reference(reference_key='#',
                        reference_text='# notation is used to (remember) input values.')
        r_1.save()
        r_2 = Reference(reference_key='String Notation',
                        reference_text='String Notations: Empty_String for empty string, o for concatenation, <E> for '
                                       'string containing a single entry E, and |S| for the length of string S.')
        r_2.save()

        r_1.lesson.add(l_1)
        r_1.lesson.add(l_2)

        r_2.lesson.add(l_1)
        """
