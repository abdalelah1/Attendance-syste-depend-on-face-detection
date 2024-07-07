# Generated by Django 5.0.6 on 2024-07-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0006_course_practical_sessions_per_week_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="college",
            name="location",
        ),
        migrations.AddField(
            model_name="attendancerecord",
            name="week_number",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
