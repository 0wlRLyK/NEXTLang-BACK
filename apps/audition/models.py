from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from apps.courses.constants import LearningLevels
from apps.courses.models import Exercise, Section, Topic

User = get_user_model()


class AuditionSection(Section):
    pass


class AuditionTopic(Topic):
    section = models.ForeignKey(AuditionSection, on_delete=models.SET_NULL, null=True)


class AuditionExercise(Exercise):
    topic = models.ForeignKey(AuditionTopic, on_delete=models.SET_NULL, null=True)


class AuditionExerciseVariant(models.Model):
    exercise = models.ForeignKey(
        AuditionExercise, related_name="variants", on_delete=models.CASCADE
    )
    options = JSONField()
    answer = JSONField()


class UserAuditionTopic(models.Model):
    user_course = models.ForeignKey(
        "courses.UserCourse", related_name="audition_topics", on_delete=models.CASCADE
    )
    topic = models.ForeignKey(AuditionTopic, on_delete=models.CASCADE)
    points = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Earned points"
    )
    exercises = models.ManyToManyField("courses.ExerciseType", blank=True)
    is_theory_read = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    learning_level = models.CharField(
        max_length=20, choices=LearningLevels.choices, default=LearningLevels.STARTED
    )
    updated_at = models.DateTimeField(auto_now=True)


class UserAuditionExerciseAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(AuditionExercise, on_delete=models.CASCADE)
    attempts_count = models.PositiveIntegerField(default=0)
    variant = models.ForeignKey(AuditionExerciseVariant, on_delete=models.CASCADE)
    points = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Earned points"
    )
