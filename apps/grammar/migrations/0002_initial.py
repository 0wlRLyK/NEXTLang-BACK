# Generated by Django 4.2.7 on 2023-11-11 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("courses", "0002_initial"),
        ("grammar", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="usergrammarexerciseattempt",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="usergrammarexerciseattempt",
            name="variant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="grammar.grammarexercisevariant",
            ),
        ),
        migrations.AddField(
            model_name="grammartopic",
            name="section",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="grammar.grammarsection",
            ),
        ),
        migrations.AddField(
            model_name="grammarsection",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="courses.course",
            ),
        ),
        migrations.AddField(
            model_name="grammarsection",
            name="level",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="courses.level",
            ),
        ),
        migrations.AddField(
            model_name="grammarexercisevariant",
            name="exercise",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="variants",
                to="grammar.grammarexercise",
            ),
        ),
        migrations.AddField(
            model_name="grammarexercise",
            name="exercise_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="courses.exercisetype",
            ),
        ),
        migrations.AddField(
            model_name="grammarexercise",
            name="topic",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="grammar.grammartopic",
            ),
        ),
    ]
