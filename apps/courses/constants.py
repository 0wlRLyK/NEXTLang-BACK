from enum import StrEnum
from typing import Literal

from django.db.models import TextChoices


class LearningLevels(TextChoices):
    STARTED = "started", "started"
    IN_PROGRESS = "in_progress", "in_progress"
    LEARNED = "learned", "learned"


class TopicTypes(TextChoices):
    GRAMMAR = "grammar", "grammar"
    AUDITION = "audition", "audition"
    VOCABULARY = "vocabulary", "vocabulary"


class LearningSpheres(StrEnum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    AUDITION = "audition"


SphereLiteral = Literal[
    LearningSpheres.GRAMMAR, LearningSpheres.AUDITION, LearningSpheres.VOCABULARY
]
