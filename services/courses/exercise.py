from abc import ABC, abstractmethod
from typing import Dict, Union

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from apps.audition.models import AuditionExerciseVariant, UserAuditionExerciseAttempt
from apps.grammar.models import GrammarExerciseVariant, UserGrammarExerciseAttempt
from apps.users.models import User
from services.courses.exceptions import (
    InvalidAnswerSchemaException,
    NoExerciseOptionsAvailableException,
    WrongAnswerException,
)


class ExerciseAttemptFactory(ABC):
    @abstractmethod
    def create(self, user, exercise, variant, **kwargs):
        ...

    @abstractmethod
    def check_answer(self, user, exercise, variant):
        ...

    @abstractmethod
    def set_next_variant(self):
        ...


class AuditionAttemptFactory(ExerciseAttemptFactory):
    def create(self, user, exercise, variant, **kwargs):
        variant = ExerciseVariantService.get_random_variant(
            AuditionExerciseVariant, exercise
        )
        return UserAuditionExerciseAttempt.objects.create(
            user=user, exercise=exercise, variant=variant, attempts_count=0, points=0
        )


class GrammarAttemptFactory(ExerciseAttemptFactory):
    def create(self, user, exercise, **kwargs):
        variant = ExerciseVariantService.get_random_variant(
            GrammarExerciseVariant, exercise
        )
        return UserGrammarExerciseAttempt.objects.create(
            user=user, exercise=exercise, variant=variant, attempts_count=0, points=0
        )

    # def check_answer(self, user, exercise, variant):


class VocabularyAttemptFactory(ExerciseAttemptFactory):
    def create(self, user, exercise, variant, **kwargs):
        return None


class ExerciseAttemptService:
    def __init__(self, user: User):
        self.user = user

        self.factory_mapping = {
            "audition": AuditionAttemptFactory(),
            "grammar": GrammarAttemptFactory(),
            "vocabulary": VocabularyAttemptFactory(),
        }

    def create(self, type, user, exercise, variant, **kwargs):
        factory = self.factory_mapping.get(type)
        if not factory:
            raise ValueError("Invalid exercise type")
        return factory.create(user, exercise, variant, **kwargs)


class ExerciseVariantService:
    @staticmethod
    def get_random_variant(variant_model, exercise):
        variants = variant_model.objects.filter(exercise=exercise)
        if not variants.exists():
            raise NoExerciseOptionsAvailableException
        return variants.order_by("?").first()


class CheckAnswerVariantService:
    def __init__(
        self,
        exercise_attempt: Union[
            UserAuditionExerciseAttempt, UserGrammarExerciseAttempt
        ],
        user_answer: Dict,
    ):
        self.exercise_attempt = exercise_attempt
        self.user_answer = user_answer
        self.answer_schema = self._get_answer_schema()

    def _validate_json_schema(self):
        try:
            validate(instance=self.user_answer, schema=self.answer_schema)
        except ValidationError:
            raise InvalidAnswerSchemaException

    def _validate_answer(self):
        correct_answer = self._get_correct_answer()
        if not self.user_answer == correct_answer:
            raise WrongAnswerException

    def _get_answer_schema(self):
        return self.exercise_attempt.exercise.exercise_type.answer_schema

    def _get_correct_answer(self):
        return self.exercise_attempt.variant

    def check(self) -> bool:
        self._validate_json_schema()
        self._validate_answer()
        return True
