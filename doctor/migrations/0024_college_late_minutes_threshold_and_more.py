# Generated by Django 5.0.6 on 2024-07-20 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0023_course_college"),
    ]

    operations = [
        migrations.AddField(
            model_name="college",
            name="late_minutes_threshold",
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name="college",
            name="late_to_absence_threshold",
            field=models.IntegerField(default=2),
        ),
        migrations.AlterUniqueTogether(
            name="enrollment",
            unique_together={("student", "course")},
        ),
    ]
