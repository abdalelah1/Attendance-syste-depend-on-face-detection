from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import *
from random import randint
from django.db.models import Q
from .recognize_student import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    user = request.user
    if user.is_staff:
        logout(request)
        redirect('home')
    doctor = get_object_or_404(Doctor, id=request.user.doctor.id)
    courses = doctor.course_set.all()  # Assuming Doctor has a related_name 'course_set' for courses
    courses = Course.objects.filter(doctor=doctor)   
    doctor_courses_data = {}

    for course in courses:
        enrolled_students = Enrollment.objects.filter(course=course)
        # Get students with warning (assuming warning_threshold is a decimal field in College)
        warning_students = []
        for enrollment in enrolled_students:
            attendance_summary = AttendanceSummary.objects.filter(student=enrollment.student, course=course).first()

            if attendance_summary and float(attendance_summary.percentage) >= float(course.college.warning_threshold) and float(attendance_summary.percentage) < float(course.college.deprivation_threshold) :
                
                warning_students.append({
                    'student_name': enrollment.student.name,
                    'student_id': enrollment.student.id,
                    'attendance_percentage': attendance_summary.percentage,
                })

        # Get deprived students
        deprived_students = []
        for enrollment in enrolled_students:
            attendance_summary = AttendanceSummary.objects.filter(student=enrollment.student, course=course).first()
            if attendance_summary and attendance_summary.percentage >= course.college.deprivation_threshold:
                deprived_students.append({
                    'student_name': enrollment.student.name,
                    'student_id': enrollment.student.id,
                    'attendance_percentage': attendance_summary.percentage,
                })

        doctor_courses_data[course] = {
            'enrolled_students': [enrollment.student for enrollment in enrolled_students],
            'warning_students': warning_students,
            'deprived_students': deprived_students,
        }

    context = {
        'doctor': doctor,
        'courses':courses,
        'doctor_courses_data': doctor_courses_data,
    }

    return render (request,'dashboard/dashboard.html',context)
@login_required
def home(request):
    doctor = request.user.doctor
    courses = Course.objects.filter(doctor=doctor)   
    context = {
        'courses':courses,
    }
    return render(request, 'index/index.html', context)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin:index')
            login(request, user)
            return redirect('home') 
        else:
            # Return an 'invalid login' error message
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login/login.html')

def weekly_attendance(request, course_id, week_number):
    week_number = int(week_number) + 1
    doctor = request.user.doctor

    courses = Course.objects.filter(doctor=doctor)
    course = get_object_or_404(Course, id=course_id)
    for student in Student.objects.all():
        calculate_absence_percentage(student,course)
    enrollments = Enrollment.objects.filter(course=course)
    attendance_records = AttendanceRecord.objects.filter(course=course, week_number=week_number)

    # إنشاء قاموس لربط الطلاب بسجلات الحضور
    attendance_dict = {record.student.id: record for record in attendance_records}

    # دمج قائمة الطلاب مع سجلات الحضور ومنع التكرار
    student_attendance = []
    added_students = set()

    for enrollment in enrollments:
        student = enrollment.student
        
        # الحصول على ملخص الحضور
        attendance_summary = AttendanceSummary.objects.filter(student=student, course=course).first()
        
        # التحقق مما إذا كان الطالب قد أضيف مسبقًا
        if student.id not in added_students:
            attendance_record = attendance_dict.get(student.id)
            student_attendance.append({
                'student': student,
                'attendance_record': attendance_record,
                'present': attendance_record.present if attendance_record else None,
                'attendance_summary': attendance_summary  
            })
            added_students.add(student.id)
    
    context = {
        'course': course,
        'student_attendance': student_attendance,
        'week_number': week_number,
        'course_id': course_id,
        'courses': courses,
    }
    return render(request, 'weekly_attendance/weekly_attendance.html', context)

def update_attendance(request, student_id, week_number, course_id):
    if request.method == 'POST':
        attendance_status = request.POST.get('attendance') == 'present'
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        attendance_record, created = AttendanceRecord.objects.update_or_create(
            student=student,
            course=course,
            week_number=int(week_number),
            defaults={'present': attendance_status}
        )
        calculate_absence_percentage(student,course)
        return redirect('weekly_attendance', course_id=course.id, week_number=int(week_number)-1)
def photo_capture(request,course_id,week_number ):
    course=Course.objects.get(id=course_id)
    context={
        'course':course,
        'week_number':week_number,
    }
    return render(request,'photo_capture/photo_capture.html',context)
@csrf_exempt
def receive_photo(request):
    if request.method == 'POST':
        data = request.POST.get('image')
        week_number = request.POST.get('week_number')
        course_id = request.POST.get('course_id')

        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp', 'temp_image.' + ext)
        with open(temp_image_path, 'wb') as f:
            f.write(image_data.read())

        student_id = recognize_student(temp_image_path)
        os.remove(temp_image_path)

        if student_id:
            student = get_object_or_404(Student, student_id=student_id)
            course = get_object_or_404(Course, id=course_id)
            if not Enrollment.objects.filter(student=student, course=course).exists():
                return JsonResponse({'message': 'Student is not enrolled in this course!'})

            attendance_time = timezone.now()  # Get current time with timezone
            print('attendance_time',attendance_time)
            college = course.college

            first_attendance_record = AttendanceRecord.objects.filter(course=course, week_number=week_number).order_by('date').first()

            if first_attendance_record:
                # Ensure that both dates are timezone-aware
                lecture_start_time =first_attendance_record.date
                print("First attendance record date and time:", first_attendance_record.date)
                print("Lecture start time:", lecture_start_time.time())
            else:
                lecture_start_time = attendance_time  # If no record found, use current time

            # Make sure lecture_start_time is timezone-aware
            if timezone.is_naive(lecture_start_time):
                lecture_start_time = timezone.make_aware(lecture_start_time)

            attendance_record, created = AttendanceRecord.objects.get_or_create(
                student=student,
                course=course,
                week_number=week_number,
                defaults={'present': True}
            )

            if not created:
                attendance_record.present = True

            late_threshold = college.late_minutes_threshold  # Number of minutes to consider late
            absence_threshold = 10  # Number of minutes to consider absent

            # Ensure attendance_time is timezone-aware
            if timezone.is_naive(attendance_time):
                attendance_time = timezone.make_aware(attendance_time)

            if attendance_time > lecture_start_time + timedelta(minutes=late_threshold):
                attendance_record.is_late = True
            else:
                  attendance_record.is_late = False

            attendance_record.save()

            calculate_absence_percentage(student, course)
            
            return JsonResponse({'message': f'Photo received successfully! Student Name: {student.name}, Student ID: {student.student_id}'})
        else:
            return JsonResponse({'message': 'Student not recognized!'})
def logout_view(request):
    logout(request)
    return redirect('home')
def calculate_absence_percentage(student, course):
    # الحصول على شروط الدورة المتعلقة بالكلية
    college = course.college
    late_minutes_threshold = college.late_minutes_threshold
    late_to_absence_threshold = college.late_to_absence_threshold

    # حساب عدد التأخيرات وعدد الأسابيع التي يعتبر فيها الطالب غائباً
    late_count = AttendanceRecord.objects.filter(student=student, course=course, is_late=True).count()
    absent_weeks = AttendanceRecord.objects.filter(student=student, course=course, present=False).count()

    # تحويل التأخيرات إلى عدد غيابات
    late_as_absences = late_count // late_to_absence_threshold

    # تحديد نسبة الغياب بناءً على نوع الدورة
    if course.course_type == 'theoretical':
        course_conditions = course.conditions
        absence_percentage = (absent_weeks + late_as_absences) * float(course_conditions.theoretical_percentage)

        # حساب نسبة الغياب للدورة العملية المرتبطة إذا كانت موجودة
        practical_course = course.practical_courses.first()
        if practical_course:
            practical_absent_weeks = AttendanceRecord.objects.filter(student=student, course=practical_course, present=False).count()
            practical_late_count = AttendanceRecord.objects.filter(student=student, course=practical_course, is_late=True).count()
            practical_late_as_absences = practical_late_count // late_to_absence_threshold
            practical_absence_percentage = (practical_absent_weeks + practical_late_as_absences) * float(practical_course.parent_course.conditions.practical_percentage)
            total_absence_percentage = absence_percentage + practical_absence_percentage
        else:
            total_absence_percentage = absence_percentage
    else:
        course_conditions = course.parent_course.conditions
        absence_percentage = (absent_weeks + late_as_absences) * float(course_conditions.practical_percentage)

        # حساب نسبة الغياب للدورة النظرية المرتبطة إذا كانت موجودة
        theoretical_course = course.parent_course
        theoretical_absent_weeks = AttendanceRecord.objects.filter(student=student, course=theoretical_course, present=False).count()
        theoretical_late_count = AttendanceRecord.objects.filter(student=student, course=theoretical_course, is_late=True).count()
        theoretical_late_as_absences = theoretical_late_count // late_to_absence_threshold
        theoretical_absence_percentage = (theoretical_absent_weeks + theoretical_late_as_absences) * float(theoretical_course.conditions.theoretical_percentage)
        total_absence_percentage = absence_percentage + theoretical_absence_percentage

    print(total_absence_percentage)
    attendance_summary, created = AttendanceSummary.objects.get_or_create(
        student=student,
        course=course,
        defaults={'percentage': total_absence_percentage}
    )

    if not created:
        attendance_summary.percentage = total_absence_percentage
        attendance_summary.save()

def student_list(request, course_id, status):
    doctor = request.user.doctor
    courses = Course.objects.filter(doctor=doctor)
    course = get_object_or_404(Course, id=course_id)
    enrolled_students = Enrollment.objects.filter(course=course)
    
    students = []
    
    if status == 'enrolled':
        for enrollment in enrolled_students:
            attendance_summary = AttendanceSummary.objects.filter(student=enrollment.student, course=course).first()
            if attendance_summary:
                students.append({
                    'student': enrollment.student,
                    'attendance_percentage': attendance_summary.percentage
                })
            else:
                students.append({
                    'student': enrollment.student,
                    'attendance_percentage': None
                })
    elif status == 'warned':
        for enrollment in enrolled_students:
            attendance_summary = AttendanceSummary.objects.filter(student=enrollment.student, course=course).first()
            if attendance_summary and float(attendance_summary.percentage) >= float(course.college.warning_threshold) and float(attendance_summary.percentage) < float(course.college.deprivation_threshold) :
                students.append({
                    'student': enrollment.student,
                    'attendance_percentage': attendance_summary.percentage
                })
    elif status == 'deprived':
        for enrollment in enrolled_students:
            attendance_summary = AttendanceSummary.objects.filter(student=enrollment.student, course=course).first()
            if attendance_summary and attendance_summary.percentage >= course.college.deprivation_threshold:
                students.append({
                    'student': enrollment.student,
                    'attendance_percentage': attendance_summary.percentage
                })
    
    context = {
        'course': course,
        'students': students,
        'status': status,
        'courses': courses
    }
    return render(request, 'students_list/students_list.html', context)
def end_section(request, course_id, week_number):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    
    for enrollment in enrollments:
        student = enrollment.student
        attendance_record, created = AttendanceRecord.objects.get_or_create(
            student=student, 
            course=course, 
            week_number=week_number,
            defaults={'present': False,'is_late': None}
        )
        if created:
            attendance_record.present = False
            attendance_record.is_late=None
            attendance_record.save()

    return redirect('weekly_attendance', course_id=course_id, week_number=week_number - 1)
