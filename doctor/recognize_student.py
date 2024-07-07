import face_recognition
import pickle
import os
import cv2
from django.conf import settings
from .models import Student
import numpy as np
def train_and_store_encodings():
    # الحصول على كل الطلاب من قاعدة البيانات
    students = Student.objects.all()
    imgList = []
    studentID = []

    # تحميل صور الطلاب وتخزينها في قائمة
    for student in students:
        if student.photo:
            img_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)
            img = cv2.imread(img_path)
            if img is not None:
                imgList.append(img)
                studentID.append(student.student_id)

    # إيجاد الترميزات لكل الصور
    encodelistKnown = find_encodings(imgList)
    encodelistKnownID = [encodelistKnown, studentID]

    # تأكد من أن المجلد موجود، وإن لم يكن قم بإنشائه
    if not os.path.exists(settings.STATIC_ROOT):
        os.makedirs(settings.STATIC_ROOT)

    # تخزين الترميزات في ملف داخل مجلد static
    file_path = os.path.join(settings.STATIC_ROOT, 'EncodeFile.p')
    with open(file_path, 'wb') as file:
        pickle.dump(encodelistKnownID, file)

def find_encodings(imagesList):
    encodelist = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist
def recognize_student(image_path):
    # تحميل الملف المخزن سابقًا
    file_path = os.path.join(settings.STATIC_ROOT, 'EncodeFile.p')
    with open(file_path, 'rb') as file:
        encodelistKnownID = pickle.load(file)

    encodelistKnown, studentID = encodelistKnownID

    # تحميل صورة الإدخال
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # إيجاد ترميزات الوجه في صورة الإدخال
    faces_cur_frame = face_recognition.face_locations(img_rgb)
    encodes_cur_frame = face_recognition.face_encodings(img_rgb, faces_cur_frame)

    for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encodelistKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodelistKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            student_id = studentID[matchIndex]
            return student_id

    return None