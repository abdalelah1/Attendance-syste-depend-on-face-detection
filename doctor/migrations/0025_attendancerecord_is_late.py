# Generated by Django 5.0.6 on 2024-07-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0024_college_late_minutes_threshold_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendancerecord",
            name="is_late",
            field=models.BooleanField(default=False),
        ),
    ]
