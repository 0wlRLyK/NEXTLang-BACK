# Generated by Django 4.2.7 on 2023-11-15 16:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_usercourse_level"),
        ("audition", "0004_alter_auditionexercise_iterations_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="auditiontopic",
            options={"ordering": ("section__order", "order")},
        ),
        migrations.AddField(
            model_name="userauditiontopic",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userauditiontopic",
            name="is_learning",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name="userauditiontopic",
            unique_together={("user_course", "is_learning")},
        ),
    ]
