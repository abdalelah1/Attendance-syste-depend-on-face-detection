# Generated by Django 5.0.6 on 2024-06-28 01:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_remove_student_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekly_percentage', models.DecimalField(decimal_places=2, default=6.0, max_digits=5)),
                ('total_weeks', models.PositiveIntegerField(default=16)),
                ('theoretical_percentage', models.DecimalField(decimal_places=2, default=4.0, max_digits=5)),
                ('practical_percentage', models.DecimalField(decimal_places=2, default=2.0, max_digits=5)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='doctor.course')),
            ],
        ),
    ]
