from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify
from ordered_model.models import OrderedModel

from apps.courses.constants import LearningLevels, TopicTypes


class Language(models.Model):
    """Language model"""

    name = models.CharField(max_length=25)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    """Course model"""

    name = models.CharField(max_length=200)
    from_language = models.ForeignKey(
        Language,
        related_name="users_language_courses",
        verbose_name="Native language of student",
        on_delete=models.SET_NULL,
        null=True,
    )
    to_language = models.ForeignKey(
        Language,
        related_name="studied_language_courses",
        verbose_name="Studied language",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


class Level(models.Model):
    """Model of complexity level"""

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class ExerciseType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, default=None, unique=True, blank=True)
    conditions = RichTextField()
    points = models.DecimalField(max_digits=5, decimal_places=2)
    repeat_points = models.DecimalField(max_digits=5, decimal_places=2)
    iterations = models.PositiveSmallIntegerField(
        default=1,
        help_text="The required number of iterations to complete the exercise",
    )
    topic_type = ArrayField(
        models.CharField(
            max_length=20,
            choices=TopicTypes.choices,
        ),
        size=5,
        null=True,
        blank=True,
    )
    is_reset_points_after_error = models.BooleanField(default=True)
    question_schema = models.JSONField(default=None)
    answer_schema = models.JSONField(default=None)
    example = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Section(OrderedModel):
    course = models.ForeignKey("courses.Course", on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey("courses.Level", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = RichTextField()

    order_with_respect_to = ("course", "level")

    class Meta(OrderedModel.Meta):
        abstract = True

    def __str__(self):
        return self.name


class Topic(OrderedModel):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = RichTextField()
    slug = models.SlugField(null=True, default=None, unique=True)
    required_points = models.PositiveSmallIntegerField(default=0)
    order_with_respect_to = "section"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(OrderedModel.Meta):
        abstract = True
        ordering = ("section__order", "order")


class Exercise(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(null=True, default=None, blank=True)
    conditions = RichTextField()
    exercise_type = models.ForeignKey(
        "courses.ExerciseType", on_delete=models.SET_NULL, null=True
    )
    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="You can overwrite default value of points for particular exercise",
        blank=True,
    )
    iterations = models.PositiveSmallIntegerField(
        default=1,
        help_text="The required number of iterations to complete the exercise",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.exercise_type.slug
        if not self.points:
            self.points = self.exercise_type.points
        if not self.iterations:
            self.iterations = self.exercise_type.iterations
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-points",)
        abstract = True


class UserCourse(models.Model):
    user = models.ForeignKey(
        "users.User", related_name="courses", on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, default=None)
    total_grammar_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total_vocabulary_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total_audition_points = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    is_default = models.BooleanField(default=False, db_index=True)
    total_passed_grammar_topics = models.PositiveIntegerField(default=0)
    total_passed_audition_topics = models.PositiveIntegerField(default=0)
    total_passed_words = models.PositiveIntegerField(default=0)
    total_passed_word_sets = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [["user", "is_default"]]


class UserDay(models.Model):
    date = models.DateField(auto_now=True)
    user_course = models.ForeignKey(
        UserCourse, related_name="days", on_delete=models.CASCADE
    )
    total_grammar_points = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    total_vocabulary_points = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    total_audition_points = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )

    total_passed_grammar_topics = models.PositiveIntegerField(default=0)
    total_passed_audition_topics = models.PositiveIntegerField(default=0)
    total_passed_words = models.PositiveIntegerField(default=0)
    total_passed_word_sets = models.PositiveIntegerField(default=0)

    is_old_material_mastered = models.BooleanField(default=False)
    is_new_material_learned = models.BooleanField(default=False)


class UserTopic(models.Model):
    user_course = None
    topic = None
    is_theory_read = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    is_learning = models.BooleanField(default=False)
    points = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0, verbose_name="Earned points"
    )
    exercises = models.ManyToManyField("courses.ExerciseType", blank=True)
    learning_level = models.CharField(
        max_length=20, choices=LearningLevels.choices, default=LearningLevels.STARTED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
