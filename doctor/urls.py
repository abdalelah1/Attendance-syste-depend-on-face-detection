from django.contrib import admin
from django.urls import path ,include
from .views import *

urlpatterns = [
path('', view=dashboard,name='home'),
path('dashboard/',dashboard,name='dashboard'),
path('login/',login_view,name='login'),
path('logout/',logout_view,name='logout'),
path('weekly/attendance/<str:course_id>/<str:week_number>/',weekly_attendance,name='weekly_attendance'),
path('update/attendance/<int:student_id>/<int:week_number>/<str:course_id>/', update_attendance, name='update_attendance'),
path('receive_photo/', receive_photo, name='receive_photo'),
path('photo_capture/<str:course_id>/<str:week_number>/', photo_capture, name='photo_capture'),
path('students/<int:course_id>/<str:status>/', student_list, name='student_list'),




]