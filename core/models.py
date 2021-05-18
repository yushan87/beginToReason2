"""
This module contains model templates for the "core" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.db import models


class AlternateType(models.IntegerChoices):
    """
    Note: this is NOT a table in the database! This is a helper class for enumeration of types.
    """
    CORRECT = -1, 'Correct'
    DEFAULT = 0, 'Default'
    SIMPLIFY = 1, 'Simplify'
    SELF_REFERENCE = 2, 'Self Reference'
    CONCRETE = 3, "Used Concrete Value as Answer"
    INITIAL = 4, 'Missing # Symbol'
    ALGEBRA = 5, 'Algebra'
    VARIABLE = 6, 'Variable'


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
    Contains a model of Incorrect Answers. These are answers that when input on lessons, signify that the lesson should
    be redirected into an alternate lesson of their type. The type is recorded as an enumeration in the M2M relation
    LessonIncorrectAnswers.

    @param models.Model The base model
    """
    answer_text = models.CharField(max_length=200)  # Has a semicolon at the end!!!

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
    feedback_type = models.IntegerField(choices=AlternateType.choices, blank=False, null=False)
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
    correct = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    correct_feedback = models.TextField(default='Proceeding to the next lesson.')
    feedback = models.ManyToManyField(Feedback, blank=True)

    is_walkthrough = models.BooleanField(default=False)
    can_mutate = models.BooleanField(default=False)
    screen_record = models.BooleanField(default=False)
    audio_record = models.BooleanField(default=False)
    audio_transcribe = models.BooleanField(default=False)

    def __str__(self):
        """"
        function __str__ is called to display the Lesson name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.lesson_title


class LessonIncorrectAnswers(models.Model):
    """
    Model that is a many-to-many between lessons and their incorrect answers. Contains an enumeration so we can store
    alternate types in the database in an efficient manner.
    """
    lesson = models.ForeignKey(Lesson, blank=False, null=False, on_delete=models.CASCADE)
    answer = models.ForeignKey(IncorrectAnswer, blank=False, null=False, on_delete=models.PROTECT)
    type = models.IntegerField(choices=AlternateType.choices, blank=False, null=False)


class LessonSet(models.Model):
    """
    Contains a model of a lesson set
    Name - For identifying purposes.
    Lessons - The linked lessons for the model
    First In Set - Identifying the first lesson in the set
    Description - To display on the catalog
    Index - To order in main set

    @param models.Model The base model
    """
    set_name = models.CharField(max_length=50)
    first_in_set = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    set_description = models.TextField(default="This set is designed to further your understanding")
    index_in_set = models.IntegerField(default=0)

    def __str__(self):
        """"
        function __str__ is called to display the Lesson name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.set_name

    def lesson_by_index(self, index):
        """"
        function lesson_by_index returns the lesson at the given index in the lesson set
        Returns:
            Lesson
        """
        try:
            return LessonSetLessons.objects.get(lesson_set=self, index=index).lesson
        except LessonSetLessons.DoesNotExist:
            return None

    def lessons(self):
        """"
        function lessons returns ordered list of the lessons within the lesson set
        Returns:
            Array of Lessons
        """
        lesson_list = []
        for relation in LessonSetLessons.objects.filter(lesson_set=self).order_by('index').all():
            lesson_list.append(relation.lesson)
        return lesson_list

    def length(self):
        """"
        function length returns how many lessons a lesson set has
        Returns:
            Integer representing length of set
        """
        return LessonSetLessons.objects.filter(lesson_set=self).count()


class LessonAlternate(models.Model):
    """
    A many-to-many between lessons (the primary, main lessons) and their alternate sets. Also includes an enumeration
    of the incorrect answer type that should be linked to the set. If no relation is present for a type, there is no
    alternate and progress is normal. If the relation exists, when a user triggers the type with an incorrect answer,
    the user will progress through the alternate set referenced, and when the user is done with the alternate, they
    will be at the NEXT lesson after the triggering lesson (i.e. alternates replace the triggering lesson)

    @param models.Model The base model
    """

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=False)
    alternate_set = models.ForeignKey(LessonSet, on_delete=models.PROTECT, null=False)
    replace = models.BooleanField(null=False, blank=False)  # If true, if alt lesson A is called on lesson 1, after A
    # is completed the user goes to lesson 2. If false, they would have to complete A, then 1, then 2.
    type = models.IntegerField(choices=AlternateType.choices, blank=False, null=False)


class LessonSetLessons(models.Model):
    """
    Many to Many between Lesson Sets
    and Lessons.
    Index - placement of lesson within lesson set

    @param models.Model The base model
    """
    lesson_set = models.ForeignKey(LessonSet, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)  # We do NOT want to cascade here - it will destroy indexing!
    index = models.IntegerField()  # No defaults, never blank, never null.


class MainSet(models.Model):
    """
    Contains a model of a main set
    Name - For identifying purposes.
    Lessons - The linked lessons for the model
    Show - Boolean for visible or not
    Description - To display on the catalog

    @param models.Model The base model
    """
    set_name = models.CharField(max_length=50)
    set_description = models.TextField(default="This set is designed to further your understanding")
    show = models.BooleanField(default=False)

    def __str__(self):
        """"
        function __str__ is called to display the set name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.set_name

    def set_by_index(self, index):
        """"
        function set_by_index returns the lesson set at the given index in the main set
        Returns:
            Lesson set
        """
        try:
            return MainSetLessonSets.objects.get(main_set=self, index=index).lesson_set
        except MainSetLessonSets.DoesNotExist:
            return None

    def sets(self):
        """"
        function set_by_index returns ordered list of the lesson sets within the main set
        Returns:
            Array of Lesson sets
        """
        set_list = []
        for relation in MainSetLessonSets.objects.filter(main_set=self).order_by('index').all():
            set_list.append(relation.lesson_set)
        return set_list

    def length(self):
        """"
        function length returns how many lesson sets a main set has
        Returns:
            Integer representing length of main set
        """
        return MainSetLessonSets.objects.filter(main_set=self).count()


class MainSetLessonSets(models.Model):
    """
    Many to Many between Main Sets
    and Lesson Sets.
    Index - placement of lesson set within main set

    @param models.Model The base model
    """
    main_set = models.ForeignKey(MainSet, on_delete=models.CASCADE)
    lesson_set = models.ForeignKey(LessonSet, on_delete=models.PROTECT)  # We do NOT want to cascade here as
    # it will destroy indexing!
    index = models.IntegerField()  # No defaults, never blank, never null.
