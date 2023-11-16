from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from apps.courses.models import Exercise, Section, Topic, UserTopic

User = get_user_model()


class AuditionSection(Section):
    pass


class AuditionTopic(Topic):
    section = models.ForeignKey(
        AuditionSection, related_name="topics", on_delete=models.SET_NULL, null=True
    )


class AuditionExercise(Exercise):
    topic = models.ForeignKey(
        AuditionTopic,
        on_delete=models.SET_NULL,
        null=True,
    )


class AuditionExerciseVariant(models.Model):
    exercise = models.ForeignKey(
        AuditionExercise, related_name="variants", on_delete=models.CASCADE
    )
    options = JSONField()
    answer = JSONField()


class UserAuditionTopic(UserTopic):
    user_course = models.ForeignKey(
        "courses.UserCourse",
        related_name="audition_topics",
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        AuditionTopic, related_name="user_topics", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user_course", "is_learning")


class UserAuditionExerciseAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(AuditionExercise, on_delete=models.CASCADE)
    attempts_count = models.PositiveIntegerField(default=0)
    variant = models.ForeignKey(AuditionExerciseVariant, on_delete=models.CASCADE)
    points = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Earned points"
    )
