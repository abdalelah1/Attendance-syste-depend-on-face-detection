from django.contrib import admin
from .models import College, Doctor, Student, Course, Enrollment, AttendanceRecord, AttendanceSummary, CourseConditions

# تسجيل نموذج College
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# تسجيل نموذج Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'college', 'email', 'user')
    search_fields = ('name', 'email')
    list_filter = ('college',)




# تسجيل نموذج Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'theoretical_doctor', 'practical_doctor', 'theoretical_sessions_per_week', 'practical_sessions_per_week')
    search_fields = ('name',)
    list_filter = ('theoretical_doctor', 'practical_doctor')

# تسجيل نموذج Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'enrollment_date')
    search_fields = ('student__name', 'course__name')
    list_filter = ('course',)

# تسجيل نموذج AttendanceRecord
@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'date', 'week_number', 'present')
    search_fields = ('student__name', 'course__name')
    list_filter = ('course', 'date', 'week_number', 'present')

# تسجيل نموذج AttendanceSummary
@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'week_number', 'total_classes', 'attended_classes')
    search_fields = ('student__name', 'course__name')
    list_filter = ('course', 'week_number')

# تسجيل نموذج CourseConditions
@admin.register(CourseConditions)
class CourseConditionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'weekly_percentage', 'total_weeks', 'theoretical_percentage', 'practical_percentage')
    search_fields = ('course__name',)
    list_filter = ('course',)

# إذا كنت تريد تخصيص إعدادات استيراد وتصدير
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('id', 'name', 'college', 'student_id')
    search_fields = ('name', 'student_id')
    list_filter = ('college',)


admin.site.register(Student, StudentAdmin)
