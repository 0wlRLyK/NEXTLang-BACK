from django.contrib import admin
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor

from apps.courses.forms import ExerciseTypeForm
from apps.courses.models import Course, ExerciseType, Language, Level


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    form = ExerciseTypeForm
    list_display = (
        "name",
        "points",
        "repeat_points",
        "iterations",
        "example",
        "answer_schema",
    )
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={
                    "mode": "code",
                    "modes": ["code", "form", "text", "tree", "view"],
                },
                ace_options={"readOnly": False},
            )
        }
    }


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    ...


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ...
