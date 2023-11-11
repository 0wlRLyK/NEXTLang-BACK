from django import forms

from apps.courses.constants import TopicTypes
from apps.courses.models import ExerciseType


class ExerciseTypeForm(forms.ModelForm):
    topic_type = forms.MultipleChoiceField(
        choices=TopicTypes.choices,  # Припустимо, у вашій моделі є поле MY_CHOICES
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = ExerciseType
        fields = "__all__"

    def clean_choices(self):
        return self.cleaned_data["choices"]
