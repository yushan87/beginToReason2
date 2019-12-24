from django.test import TestCase

from .models import Lesson, Reference

# Create your tests here.

class LessonModelTests(TestCase):
	def test_add_multiple_references(self):
		'''
		Ensure that lesson can contain multiple references
		'''

		L1 = Lesson(lesson_name = 'Lesson1')
		L1.save()
		L2 = Lesson(lesson_name = 'Lesson2')
		L2.save()
		L3 = Lesson(lesson_name = 'Lesson3')
		L3.save()

		R1 = Reference(reference_key = '#', reference_text = '# notation is used to (remember) input values.')
		R1.save()
		R2 = Reference(reference_key = 'String Notation', reference_text = 'String Notations: Empty_String for empty string, o for concatenation, <E> for string containing a single entry E, and |S| for the length of string S.')
		R2.save()

		R1.lesson.add(L1)
		R1.lesson.add(L2)

		R2.lesson.add(L1)