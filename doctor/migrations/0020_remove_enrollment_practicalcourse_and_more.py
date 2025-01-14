# Generated by Django 5.0.6 on 2024-07-10 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0019_attendancerecord_practicalcourse_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="enrollment",
            name="practicalCourse",
        ),
        migrations.RemoveField(
            model_name="attendancerecord",
            name="practicalCourse",
        ),
        migrations.RemoveField(
            model_name="course",
            name="practical_sessions_per_week",
        ),
        migrations.RemoveField(
            model_name="course",
            name="theoretical_doctor",
        ),
        migrations.RemoveField(
            model_name="course",
            name="theoretical_sessions_per_week",
        ),
        migrations.RemoveField(
            model_name="courseconditions",
            name="weekly_percentage",
        ),
        migrations.AddField(
            model_name="course",
            name="course_type",
            field=models.CharField(
                choices=[("theoretical", "Theoretical"), ("practical", "Practical")],
                default="theoretical",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="doctor",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="doctor.doctor",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="course",
            name="parent_course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="practical_courses",
                to="doctor.course",
            ),
        ),
        migrations.AlterField(
            model_name="enrollment",
            name="course",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="doctor.course",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="PracticalCourses",
        ),
    ]
