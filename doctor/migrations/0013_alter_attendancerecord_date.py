# Generated by Django 5.0.6 on 2024-07-05 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0012_alter_enrollment_enrollment_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendancerecord",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]