# Generated by Django 5.0.6 on 2024-07-20 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0028_alter_attendancerecord_is_late"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendancerecord",
            name="is_late",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]