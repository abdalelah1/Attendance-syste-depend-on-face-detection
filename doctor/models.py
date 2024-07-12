from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from doctor.recognize_student import train_and_store_encodings
class College(models.Model):
    name = models.CharField(max_length=255)
    warning_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=12)  # نسبة الإنذار
    deprivation_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=15)  # نسبة الحرمان
    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    college = models.ForeignKey('College', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=50, blank=True, editable=False)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Doctor)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create(username=instance.email, email=instance.email)
        # Set default password
        default_password = generate_random_password(instance.name)
        user.set_password(default_password)
        user.save()
        instance.user = user
        instance.password = default_password  # تخزين كلمة المرور في حقل كلمة المرور
        instance.save()

@receiver(post_save, sender=Doctor)
def save_user_profile(sender, instance, **kwargs):
    if instance.user:
        instance.user.email = instance.email
        instance.user.save()
class Student(models.Model):
    name = models.CharField(max_length=255)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)  # إضافة حقل الصورة

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # Check if this is a new instance
        is_new = self.pk is None
        super(Student, self).save(*args, **kwargs)
        if is_new:
            # Call your function here
            print('training')
            train_and_store_encodings()
            

class Course(models.Model):
    COURSE_TYPES = (
        ('theoretical', 'Theoretical'),
        ('practical', 'Practical'),
    )
    
    name = models.CharField(max_length=255)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, default='theoretical')
    parent_course = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='practical_courses')
    students = models.ManyToManyField(Student, through='Enrollment')
    
    def __str__(self):
        return self.name if self.course_type == 'theoretical' else f"{self.parent_course.name} Practical"

class CourseConditions(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='conditions')
    total_weeks = models.PositiveIntegerField(default=16)
    theoretical_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=4.00)
    practical_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)
    
    def __str__(self):
        return f"Conditions for {self.course.name}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    week_number = models.PositiveIntegerField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.date}"

class AttendanceSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    percentage = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.student.name} - {self.course.name} - percentage {self.percentage}%"


import random
import string

def generate_random_password(name):
    # التأكد من أن الاسم يحتوي على الأقل على حرفين
    if len(name) < 2:
        raise ValueError("Name must contain at least two characters")

    # أخذ أول حرفين من الاسم
    prefix = name[:2]

    # توليد خمسة أرقام عشوائية
    random_numbers = ''.join(random.choices(string.digits, k=5))

    # دمج الحروف والأرقام لتكوين كلمة المرور
    password = prefix + random_numbers

    return password
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"
