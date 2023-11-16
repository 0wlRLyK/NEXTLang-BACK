from ckeditor.fields import RichTextField
from django.db import models

from apps.courses.constants import LearningLevels
from apps.vocabulary.constants import PartOfSpeech


class WordSet(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.SET_NULL, null=True)
    levels = models.ManyToManyField("courses.Level", blank=True)
    name = models.CharField(max_length=200)
    description = RichTextField()
    words = models.ManyToManyField("Word", blank=True)


class Word(models.Model):
    language = models.ForeignKey(
        "courses.Language", on_delete=models.SET_NULL, null=True
    )
    word = models.CharField(max_length=200)
    definition = models.TextField()
    transcription = models.CharField(max_length=200)
    part_of_speech = models.CharField(max_length=25, choices=PartOfSpeech.choices)
    synonyms = models.ManyToManyField("self", blank=True)


class WordExample(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    sentence = models.TextField()


class WordExampleTranslation(models.Model):
    example = models.ForeignKey(WordExample, on_delete=models.CASCADE)
    language = models.ForeignKey("courses.Language", on_delete=models.CASCADE)
    sentence = models.TextField()


class WordTranslation(models.Model):
    language = models.ForeignKey(
        "courses.Language", on_delete=models.SET_NULL, null=True
    )
    word = models.CharField(max_length=200)
    definition = models.TextField()


class UserWord(models.Model):
    user_course = models.ForeignKey(
        "courses.UserCourse", related_name="words", on_delete=models.CASCADE
    )
    learning_level = models.CharField(
        max_length=20, choices=LearningLevels.choices, default=LearningLevels.STARTED
    )
    updated_at = models.DateTimeField(auto_now=True)


class UserDictionary(models.Model):
    user_course = models.ForeignKey(
        "courses.UserCourse", related_name="dictionaries", on_delete=models.CASCADE
    )
    language = models.ForeignKey("courses.Language", on_delete=models.CASCADE)
    words = models.ManyToManyField(Word, blank=True)
    name = models.CharField(max_length=20)


# class UserAuditionExerciseAttempt(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     exercise = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
#     attempts_count = models.PositiveIntegerField(default=0)
#     variant = models.ForeignKey(AuditionExerciseVariant, on_delete=models.CASCADE)
#     points = models.DecimalField(
#         max_digits=5, decimal_places=2, verbose_name="Earned points"
#     )
#     options = JSONField()
#     answer = JSONField()
