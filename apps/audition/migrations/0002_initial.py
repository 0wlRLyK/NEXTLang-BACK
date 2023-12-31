# Generated by Django 4.2.7 on 2023-11-11 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("courses", "0001_initial"),
        ("audition", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userauditiontopic",
            name="exercises",
            field=models.ManyToManyField(blank=True, to="courses.exercisetype"),
        ),
        migrations.AddField(
            model_name="userauditiontopic",
            name="topic",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="audition.auditiontopic"
            ),
        ),
        migrations.AddField(
            model_name="userauditiontopic",
            name="user_course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audition_topics",
                to="courses.usercourse",
            ),
        ),
        migrations.AddField(
            model_name="userauditionexerciseattempt",
            name="exercise",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="audition.auditionexercise",
            ),
        ),
    ]
