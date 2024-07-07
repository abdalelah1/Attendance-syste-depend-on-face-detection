from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
class College(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    college = models.ForeignKey('College', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Doctor)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create(username=instance.email, email=instance.email)
        # Set default password
        default_password = 'default_password_here'
        user.set_password(default_password)
        user.save()
        instance.user = user
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

class Course(models.Model):
    name = models.CharField(max_length=255)
    theoretical_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='theoretical_courses')
    practical_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='practical_courses', null=True, blank=True)
    students = models.ManyToManyField(Student, through='Enrollment')
    theoretical_sessions_per_week = models.PositiveIntegerField(default=0)
    practical_sessions_per_week = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    week_number = models.PositiveIntegerField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.date}"

class AttendanceSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    total_classes = models.PositiveIntegerField()
    attended_classes = models.PositiveIntegerField()

    class Meta:
        unique_together = ('student', 'course', 'week_number')

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - Week {self.week_number}"
class CourseConditions(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='conditions')
    weekly_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=6.00)
    total_weeks = models.PositiveIntegerField(default=16)
    theoretical_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=4.00)
    practical_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)

    def __str__(self):
        return f"Conditions for {self.course.name}"
