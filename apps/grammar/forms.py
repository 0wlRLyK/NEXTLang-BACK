from typing import cast

from django import forms
from django.forms import BaseInlineFormSet
from django_reactive.widget import ReactJSONSchemaFormField
from django_reactive.widget.widgets import ReactJSONSchemaFormWidget

from apps.courses.models import ExerciseType
from apps.grammar.models import GrammarExerciseVariant


class ExerciseVariantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        exercise_type = kwargs.pop("exercise_type", None)

        super().__init__(*args, **kwargs)
        # Встановлення схеми для поля форми
        if exercise_type:
            exercise_type = cast(ExerciseType, exercise_type)
            self.fields["options"] = ReactJSONSchemaFormField(
                widget=ReactJSONSchemaFormWidget(
                    schema=exercise_type.question_schema,
                    ui_schema=exercise_type.question_schema,
                )
            )
            self.fields["answer"] = ReactJSONSchemaFormField(
                widget=ReactJSONSchemaFormWidget(
                    schema=exercise_type.answer_schema,
                    ui_schema=exercise_type.answer_schema,
                )
            )

    class Meta:
        model = GrammarExerciseVariant
        fields = "__all__"


class ExerciseVariantInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        self.exercise_type = None

        if instance.pk:
            self.exercise_type = instance.exercise_type
        else:
            exercise_type_id = self.request.GET.get("exercise_type_id")
            self.exercise_type = ExerciseType.objects.get(pk=exercise_type_id)

    def _construct_form(self, i, **kwargs):
        kwargs["exercise_type"] = self.exercise_type
        return super()._construct_form(i, **kwargs)
