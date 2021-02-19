"""
This module contains model templates for the "core" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.db import models


class Code(models.Model):
    """
    Contains a model of the code, allows for the ability to reuse.

    @param models.Model The base model
    """
    code_name = models.CharField(max_length=30)
    lesson_code = models.TextField(max_length=750)

    def __str__(self):
        """
        function __str__ is called to display the name of the code

        Returns:
            str: code name
        """

        return self.code_name


class Reference(models.Model):
    """
    Contains a model of references. Each reference can be used by multiple Lessons.

    @param models.Model The base model
    """
    reference_key = models.CharField(max_length=30)
    reference_text = models.TextField(max_length=250)

    def __str__(self):
        """"
        function __str__ is called to display the reference texts. Helps for admin usability.

        Returns:
            str: reference text
        """
        return self.reference_text


class Concept(models.Model):
    """
    Contains a model of references. Each reference can be used by multiple Lessons.

    @param models.Model The base model
    """
    concept_key = models.CharField(max_length=30)
    concept_text = models.CharField(max_length=50)

    def __str__(self):
        """"
        function __str__ is called to display the reference texts. Helps for admin usability.

        Returns:
            str: reference text
        """
        return self.concept_text


class Question(models.Model):
    """
    Contains a model of Questions. Each question can be used by multiple Lessons.

    @param models.Model The base model
    """
    question_text = models.CharField(max_length=200)

    def __str__(self):
        """"
        function __str__ is called to display the question texts. Helps for admin usability.

        Returns:
            str: question text
        """
        return self.question_text


class McChoice(models.Model):
    """
    Contains a model of Multiple Choice Answers. Each choice is attached to one Question.

    @param models.Model The base model
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField(max_length=200)

    def __str__(self):
        """"
        function __str__ is called to display the multiple choice texts. Helps for admin usability.

        Returns:
            str: choice text
        """
        return self.choice_text


class Reasoning(models.Model):
    """
    Contains a model of Reasoning. There must be a question, and potential to be free response, multiple choice,
    or both. Includes an indicator for type of response needed.

    @param models.Model The base model
    """
    reasoning_name = models.CharField(max_length=30)
    reasoning_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    multiple = 'MC'
    text = 'Text'
    both = 'Both'
    none = 'None'

    response_options = [
        (multiple, 'Multiple Choice'),
        (text, 'Free Response'),
        (both, 'Multiple Choice and Free Response'),
        (none, 'None')
    ]

    reasoning_type = models.CharField(
        max_length=4,
        choices=response_options,
        default=none
    )

    # Free response has been removed, only because it does not serve a purpose. It belongs in the data collection
    # side of things.

    # free_response_text = models.CharField(max_length=100, default="Enter default message", blank=True)

    mc_set = models.ManyToManyField(McChoice, blank=True)

    def __str__(self):
        """"
        function __str__ is called to display the reasoning key. Due to the potential for multiple reasoning
        activities using the same question, the key must be the identifying feature.

        Returns:
            str: reasoning name
        """
        return self.reasoning_name


class IncorrectAnswer(models.Model):
    """
    Contains a model of Multiple Choice Answers. Each choice is attached to one Question.

    @param models.Model The base model
    """

    lesson_text = models.CharField(max_length=200, default='Lesson2')

    simplify = 'SIM'
    self = 'SELF'
    concrete = 'NUM'
    initial = 'INIT'
    algebra = 'ALG'
    variable = 'VAR'

    response_options = [
        (simplify, 'Simplify'),
        (self, 'Self Reference'),
        (concrete, 'Used Concrete Value as Answer'),
        (initial, 'Missing # Symbol'),
        (algebra, 'Algebra'),
        (variable, 'Variable')
    ]

    answer_type = models.CharField(
        max_length=4,
        choices=response_options,
        default=simplify
    )

    answer_text = models.CharField(max_length=200)

    def __str__(self):
        """"
        function __str__ is called to display the multiple choice texts. Helps for admin usability.

        Returns:
            str: choice text
        """
        return self.lesson_text + ': ' + self.answer_type + '-' + self.answer_text



class Feedback(models.Model):
    """
        Contains a model of Feedback for students.

        @param models.Model The base model
        """

    headline = models.CharField(max_length=50, default='Try Again!')

    default = 'DEF'
    correct = 'COR'
    simplify = 'SIM'
    self = 'SELF'
    concrete = 'NUM'
    initial = 'INIT'
    algebra = 'ALG'
    variable = 'VAR'
    sub_lesson = 'SUB'

    feedback_options = [
        (default, 'Default'),
        (correct, 'Correct'),
        (simplify, 'Simplify'),
        (self, 'Self Reference'),
        (concrete, 'Used Concrete Value as Answer'),
        (initial, 'Missing # Symbol'),
        (algebra, 'Algebra'),
        (variable, 'Variable'),
        (sub_lesson, 'Sub_Lesson')
    ]

    feedback_type = models.CharField(
        max_length=4,
        choices=feedback_options,
        default=default
    )

    feedback_text = models.TextField(max_length=500)

    def __str__(self):
        """"
        function __str__ is called to display the Feedback texts. Helps for admin usability.

        Returns:
            str: choice text
        """
        return self.feedback_type + ': ' + self.feedback_text



class Lesson(models.Model):
    """
    Contains a model of a Lesson.
    Name - For identifying purposes.
    Concept - May be helpful to display to the user.
    Instruction - Directions for how to perform the activity.
    Code - The code activities that student will be interacting with. Will pull from the Code model.
    Reference Set - May contain multiple references, or no references at all.
    Reason - There is only one reasoning activity allowed per Lesson. May contain mc, fr, or both.
    Screen_Record - Boolean for whether or not to record user's screen for the activity.
    Audio_Record - Boolean for whether or not to record user's audio for the activity.
    Audio_Transcribe - Boolean for whether or not to transcribe user's audio.

    @param models.Model The base model
    """
    lesson_name = models.CharField(max_length=50)
    lesson_title = models.CharField(max_length=50, default='default')
    lesson_index = models.IntegerField(default=0)
    lesson_concept = models.ManyToManyField(Concept, blank=True)
    instruction = models.TextField(default='Please complete the Confirm assertion(s) and check correctness.')
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    reference_set = models.ManyToManyField(Reference, blank=True)
    reason = models.ForeignKey(Reasoning, on_delete=models.CASCADE, blank=True, null=True)

    correct = models.CharField(max_length=50, default='Lesson To Go To')
    correct_feedback = models.TextField(default='Proceeding to the next lesson.')
    feedback = models.ManyToManyField(Feedback, blank=True)

    is_walkthrough = models.BooleanField(default=False)
    is_alternate = models.BooleanField(default=False)
    can_mutate = models.BooleanField(default=False)

    sub_lessons_available = models.BooleanField(default=False)
    incorrect_answers = models.ManyToManyField(IncorrectAnswer, blank=True)


    simplify = models.CharField(max_length=50, default='None')
    # simplify_answers = models.ManyToManyField(IncorrectAnswer, blank=True, related_name='simplify_answers')
    self_reference = models.CharField(max_length=50, default='None')
    # self_reference_answers = models.ManyToManyField(IncorrectAnswer, blank=True, related_name='self_answers')
    use_of_concrete_values = models.CharField(max_length=50, default='None')
    # use_of_concrete_values_answers = models.ManyToManyField(IncorrectAnswer, blank=True, related_name='concrete_answers')
    not_using_initial_value = models.CharField(max_length=50, default='None')
    # not_using_initial_value_answers = models.ManyToManyField(IncorrectAnswer, blank=True, related_name='initial_answers')
    algebra = models.CharField(max_length=50, default='None')
    # algebra_answers = models.ManyToManyField(IncorrectAnswer, blank=True, related_name='algebra_answers')

    variable = models.CharField(max_length=50, default='None')
    # variable_answers = models.ManyToManyField(IncorrectAnswer, blank=True, related_name='variable_answers')


    # Tool already handles syntax,so I think this should be left out.
    # syntax = models.CharField(max_length=50, default='Lesson To Go To')
    # syntax_answers = models.ManyToManyField(IncorrectAnswer, blank=True)

    screen_record = models.BooleanField(default=False)
    audio_record = models.BooleanField(default=False)
    audio_transcribe = models.BooleanField(default=False)

    # 0 correct
    # 1 correct simplify
    # 2 self reference
    # 3 use of num
    # 4 missing #
    # 5 algebra
    # 6 syntax
    # 7 var

    def __str__(self):
        """"
        function __str__ is called to display the Lesson name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.lesson_title


class LessonSet(models.Model):
    """
    Contains a model of a lesson set
    Name - For identifying purposes.
    Lessons - The linked lessons for the model
    Concepts - could be used to filter lesson sets
    Description - To display on the catalog

    @param models.Model The base model
    """
    set_name = models.CharField(max_length=50)
    lessons = models.ManyToManyField(Lesson, blank=True)
    first_in_set = models.ForeignKey(Lesson, related_name='first_in_set', on_delete=models.CASCADE, blank=True, null=True)
    set_description = models.TextField(default="This set is designed to further your understanding")
    # number_normal_lessons = models.IntegerField(default=0)

    def __str__(self):
        """"
        function __str__ is called to display the Lesson name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.set_name


class MainSet(models.Model):
    """
    Contains a model of a main set
    Name - For identifying purposes.
    Lessons - The linked lessons for the model
    Concepts - could be used to filter lesson sets
    Description - To display on the catalog

    @param models.Model The base model
    """
    set_name = models.CharField(max_length=50)
    lessons = models.ManyToManyField(LessonSet, blank=True)
    set_description = models.TextField(default="This set is designed to further your understanding")
    # set_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    show = models.BooleanField(default=False)

    def __str__(self):
        """"
        function __str__ is called to display the Lesson name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.set_name
