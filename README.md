

# Attendance Management System Using Face Recognition

Welcome to the Attendance Management System project, designed to enhance student attendance tracking through cutting-edge artificial intelligence technologies. Our advanced system integrates face recognition technology with One-Shot Learning to deliver a seamless and efficient attendance management experience. This README provides comprehensive details on setting up, using, and understanding the core features of the system.

## 💡 Overview

The Attendance Management System is an innovative solution that leverages face recognition for automatic student attendance recording. Utilizing One-Shot Learning, the system ensures high accuracy in student identification with minimal data requirements, making attendance tracking more efficient and reliable.

## 🚀 Features

### One-Shot Learning
- **Single Image Training**: The system employs One-Shot Learning to recognize students using just one image for training. This technology enables high accuracy in face recognition with minimal data input.

### Real-Time Attendance Updates
- **Automatic Updates**: As soon as a student is recognized, their attendance is automatically recorded for the respective course and week, minimizing manual intervention and reducing human errors.

### Teacher Dashboard
- **Detailed Reports**: Provides educators with a user-friendly interface to view comprehensive reports on attendance, including lists of enrolled, warned, and deprived students based on their attendance percentages.

### Automatic Attendance Logging
- **Efficient Logging**: Attendance is recorded automatically when a student is identified, eliminating manual logging and streamlining the process.

### Accurate Reports and Statistics
- **Detailed Analytics**: Offers precise reports on attendance rates, absences, and delays for each student, assisting teachers and administrators in making informed decisions.

### Absence Percentage Calculation
- **Course-Specific Calculations**: The system calculates absence percentages based on the type of course (theoretical or practical), providing accurate assessments tailored to course requirements.

### Targeted Management for Theoretical and Practical Courses
- **Specialized Interfaces**: Designed for theoretical course professors and practical course instructors, allowing them to manage and review attendance data specific to their courses.

### Warnings and Deprivation Management
- **Automated Warnings**: Monitors attendance percentages and issues warnings to students exceeding permissible absence limits. Persistent absences without justification result in deprivation from the course.

## 🛠️ Installation

### Prerequisites
- Python 3.x
- Django
- Required Python libraries (listed in `requirements.txt`)

### Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/abdalelah1/Attendance-system-depend-on-face-detection.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd Attendance-system-depend-on-face-detection
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open your web browser and navigate to `http://127.0.0.1:8000` to start using the system.

## 📜 Usage

1. **Student Enrollment**
   - Add student images and relevant data through the admin interface.

2. **Attendance Recording**
   - Students can record their attendance by facing the camera. The system automatically logs their presence.

3. **Viewing Reports**
   - Teachers can log in to view detailed attendance reports and manage student records.

4. **Managing Warnings and Deprivation**
   - The system automatically manages warnings and deprivation based on attendance records and predefined thresholds.

## 🛠️ Configuration

- **Database Settings**: Configure your database settings in `settings.py`.
- **Face Recognition Settings**: Adjust face recognition parameters if applicable.

## 📞 Contact

For any inquiries or support, please contact:
- **Email**: ataleb251@gmail.com
- **GitHub**: [abdalelah1](https://github.com/abdalelah1)



