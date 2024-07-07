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
from django.core.files.base import ContentFile
# Create your views here.
def home(request):

    doctor = request.user.doctor
    courses = Course.objects.filter(Q(theoretical_doctor=doctor) | Q(practical_doctor=doctor)) 
   
    context = {
        'courses': courses
    }
    return render(request, 'index/index.html', context)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            # Return an 'invalid login' error message
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login/login.html')

def weekly_attendance(request, course_id, week_number):
    week_number=int(week_number)+1
    doctor = request.user.doctor
    courses = Course.objects.filter(models.Q(theoretical_doctor=doctor) | models.Q(practical_doctor=doctor))
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    attendance_records = AttendanceRecord.objects.filter(course=course, week_number=week_number)

    # إنشاء قاموس لربط الطلاب بسجلات الحضور
    attendance_dict = {record.student.id: record for record in attendance_records}

# دمج قائمة الطلاب مع سجلات الحضور ومنع التكرار
    student_attendance = []
    added_students = set()

    for enrollment in enrollments:
        student = enrollment.student
        
        # التحقق مما إذا كان الطالب قد أضيف مسبقًا
        if student.id not in added_students:
            attendance_record = attendance_dict.get(student.id)
            student_attendance.append({
                'student': student,
                'attendance_record': attendance_record,
                'present': attendance_record.present if attendance_record else None
            })
            added_students.add(student.id)




    context = {
        'course': course,
        'student_attendance': student_attendance,
        'week_number': week_number,
        'course_id': course_id,
        'courses': courses
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
        return redirect('weekly_attendance', course_id=course.id, week_number=int(week_number)-1)
def photo_capture(request,course_id,week_number ,is_practical):
    course=Course.objects.get(id=course_id)
    context={
        'course':course,
        'week_number':week_number,
        'is_practical':is_practical
    }
    return render(request,'photo_capture/photo_capture.html',context)
@csrf_exempt
def receive_photo(request):
    if request.method == 'POST':
        data = request.POST.get('image')

        is_practical = request.POST.get('is_practical')
        week_number = request.POST.get('week_number')
        course_id = request.POST.get('course_id')

        format, imgstr = data.split(';base64,') 
        ext = format.split('/')[-1] 
        image_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        # Save the received image temporarily
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp', 'temp_image.' + ext)
        with open(temp_image_path, 'wb') as f:
            f.write(image_data.read())

        # Call recognize_student function with the saved image path
        student_id = recognize_student(temp_image_path)

        # Delete the temporary image file if needed
        os.remove(temp_image_path)

        if student_id:
            student = Student.objects.get(student_id=student_id)
            course = Course.objects.get(id=course_id)
            
            # Check if attendance record already exists
            attendance_record, created = AttendanceRecord.objects.get_or_create(
                student=student,
                course=course,
                week_number=week_number,
                defaults={'present': True}
            )

            if not created:
                # If the record already exists, just mark it as present
                attendance_record.present = True
                attendance_record.save()
            return JsonResponse({'message': f'Photo received successfully! Student Name: {student.name} , Student ID: {student.student_id} '})
        else:
            return JsonResponse({'message': 'Student not recognized!'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)