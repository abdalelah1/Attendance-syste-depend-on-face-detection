# Generated by Django 5.0.6 on 2024-07-09 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0017_remove_course_practical_doctor_doctor_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrollment",
            name="practicalCourse",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="doctor.practicalcourses",
            ),
        ),
        migrations.AlterField(
            model_name="enrollment",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="doctor.course",
            ),
        ),
    ]
