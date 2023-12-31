# Generated by Django 4.2.7 on 2023-11-11 10:16

import ckeditor.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="ExerciseType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "slug",
                    models.SlugField(blank=True, default=None, null=True, unique=True),
                ),
                ("conditions", ckeditor.fields.RichTextField()),
                ("points", models.DecimalField(decimal_places=2, max_digits=5)),
                ("repeat_points", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "iterations",
                    models.PositiveSmallIntegerField(
                        default=1,
                        help_text="The required number of iterations to complete the exercise",
                    ),
                ),
                (
                    "topic_type",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("grammar", "grammar"),
                                ("audition", "audition"),
                                ("vocabulary", "vocabulary"),
                            ],
                            max_length=20,
                        ),
                        blank=True,
                        null=True,
                        size=5,
                    ),
                ),
                ("is_reset_points_after_error", models.BooleanField(default=True)),
                ("question_schema", models.JSONField(default=None)),
                ("answer_schema", models.JSONField(default=None)),
                ("example", models.JSONField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                ("code", models.CharField(max_length=5, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Level",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="UserCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_grammar_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "total_vocabulary_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "total_audition_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("is_default", models.BooleanField(db_index=True, default=False)),
                ("total_passed_grammar_topics", models.PositiveIntegerField(default=0)),
                (
                    "total_passed_audition_topics",
                    models.PositiveIntegerField(default=0),
                ),
                ("total_passed_words", models.PositiveIntegerField(default=0)),
                ("total_passed_word_sets", models.PositiveIntegerField(default=0)),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="courses.course",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserDay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now=True)),
                (
                    "total_grammar_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "total_vocabulary_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "total_audition_points",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                ("total_passed_grammar_topics", models.PositiveIntegerField(default=0)),
                (
                    "total_passed_audition_topics",
                    models.PositiveIntegerField(default=0),
                ),
                ("total_passed_words", models.PositiveIntegerField(default=0)),
                ("total_passed_word_sets", models.PositiveIntegerField(default=0)),
                ("is_old_material_mastered", models.BooleanField(default=False)),
                ("is_new_material_learned", models.BooleanField(default=False)),
                (
                    "user_course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="days",
                        to="courses.usercourse",
                    ),
                ),
            ],
        ),
    ]
