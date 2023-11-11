from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from apps.courses.models import ExerciseType
from apps.grammar.forms import ExerciseVariantForm, ExerciseVariantInlineFormSet
from apps.grammar.models import (
    GrammarExercise,
    GrammarExerciseVariant,
    GrammarSection,
    GrammarTopic,
)


@admin.register(GrammarSection)
class GrammarSectionAdmin(OrderedModelAdmin):
    list_display = ("name", "course", "level", "move_up_down_links")


@admin.register(GrammarTopic)
class GrammarTopicAdmin(OrderedModelAdmin):
    list_display = ("name", "move_up_down_links")


class GrammarExerciseVariantInline(admin.StackedInline):
    model = GrammarExerciseVariant
    form = ExerciseVariantForm
    formset = ExerciseVariantInlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        kwargs["request"] = request
        return type("CustomInlineFormSet", (FormSet,), {"request": request})


@admin.register(GrammarExercise)
class GrammarExerciseAdmin(admin.ModelAdmin):
    inlines = [GrammarExerciseVariantInline]
    change_list_template = "admin/add_exercise.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["exercise_types"] = ExerciseType.objects.all()
        return super().changelist_view(request, extra_context=extra_context)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(GrammarExerciseAdmin, self).get_form(
            request, obj, change, **kwargs
        )
        form.base_fields["exercise_type"].initial = request.GET.get("exercise_type_id")
        return form


@admin.register(GrammarExerciseVariant)
class GrammarExerciseVariantAdmin(admin.ModelAdmin):
    ...


# @admin.register()
# class Admin(admin.ModelAdmin):
#     ...
