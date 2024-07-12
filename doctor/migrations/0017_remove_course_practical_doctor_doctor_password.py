# Generated by Django 5.0.6 on 2024-07-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0016_practicalcourses_doctor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="practical_doctor",
        ),
        migrations.AddField(
            model_name="doctor",
            name="password",
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
    ]
