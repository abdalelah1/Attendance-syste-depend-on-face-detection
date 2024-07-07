# Generated by Django 5.0.6 on 2024-06-28 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_course_course_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='practical_sessions_per_week',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='theoretical_sessions_per_week',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
