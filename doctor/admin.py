from django.contrib import admin
from .models import College, Doctor, Student, Course, Enrollment, AttendanceRecord, AttendanceSummary, CourseConditions
from django import forms
from django.contrib.auth.models import User, Group
# تسجيل نموذج College
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# تسجيل نموذج Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'college', 'email', 'user','password')
    search_fields = ('name', 'email')
    list_filter = ('college',)

class PracticalCourseInline(admin.TabularInline):
    model = Course
    extra = 1
    verbose_name_plural = 'Practical Courses'

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['course_type'].initial = 'practical'
        formset.form.base_fields['name'].label = 'Practical Course Name'
        return formset

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'course_type', 'parent_course_display')

    def parent_course_display(self, obj):
        if obj.course_type == 'practical' and obj.parent_course:
            return obj.parent_course.name
        return '-'
    parent_course_display.short_description = 'Parent Course'

    inlines = [PracticalCourseInline]

    def save_model(self, request, obj, form, change):
        if obj.course_type == 'practical' and obj.parent_course.course_type != 'theoretical':
            raise ValueError("A practical course can only be associated with a theoretical course.")
        
        if obj.course_type == 'practical' and not obj.parent_course:
            theoretical_course_name = f"{obj.name} Theoretical"
            theoretical_course = Course.objects.create(name=theoretical_course_name, doctor=obj.doctor, course_type='theoretical')
            obj.parent_course = theoretical_course
            
        obj.save()

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
    list_filter = ('course', 'week_number', 'present')

# تسجيل نموذج AttendanceSummary
@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'percentage', )
    search_fields = ('student__name', 'course__name')
    list_filter = ('course', 'percentage')

# تسجيل نموذج CourseConditions

# تسجيل نموذج CourseConditions
@admin.register(CourseConditions)
class CourseConditionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'total_weeks', 'theoretical_percentage', 'practical_percentage')
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
admin.site.unregister(Group)