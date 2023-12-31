# Generated by Django 4.2.7 on 2023-11-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audition", "0003_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auditionexercise",
            name="iterations",
            field=models.PositiveSmallIntegerField(
                blank=True,
                default=1,
                help_text="The required number of iterations to complete the exercise",
            ),
        ),
        migrations.AlterField(
            model_name="auditionexercise",
            name="points",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="You can overwrite default value of points for particular exercise",
                max_digits=5,
            ),
        ),
    ]
