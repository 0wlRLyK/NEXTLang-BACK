from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from apps.courses.models import Exercise, Section, Topic, UserTopic

User = get_user_model()


class GrammarSection(Section):
    ...


class GrammarTopic(Topic):
    section = models.ForeignKey(
        GrammarSection, related_name="topics", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name


class GrammarExercise(Exercise):
    topic = models.ForeignKey(GrammarTopic, on_delete=models.SET_NULL, null=True)

    # def __str__(self):
    #     return self.exercise.name


class GrammarExerciseVariant(models.Model):
    exercise = models.ForeignKey(
        GrammarExercise, related_name="variants", on_delete=models.CASCADE
    )
    options = JSONField()
    answer = JSONField()


class UserGrammarTopic(UserTopic):
    user_course = models.ForeignKey(
        "courses.UserCourse", related_name="grammar_topics", on_delete=models.CASCADE
    )
    topic = models.ForeignKey(
        GrammarTopic, related_name="user_topics", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user_course", "is_learning")


class UserGrammarExerciseAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(GrammarExercise, on_delete=models.CASCADE)
    attempts_count = models.PositiveIntegerField(default=0)
    variant = models.ForeignKey(GrammarExerciseVariant, on_delete=models.CASCADE)
    points = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Earned points"
    )
