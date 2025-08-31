from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

from .models import Teacher, Diary, Alert, Performance, Message, Event, Feedback, Report
from Home.models import Parent, Student


def teacher_register(request):
    grades = [
        "1st Grade", "2nd Grade", "3rd Grade", "4th Grade",
        "5th Grade", "6th Grade", "7th Grade", "8th Grade",
        "9th Grade", "10th Grade", "11th Grade", "12th Grade"
    ]
    divisions = ["A", "B", "C", "D", "E"]
    if request.method == 'POST':
        Teacher.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            gender=request.POST['gender'],
            date_of_birth=request.POST.get('date_of_birth'),
            subject=request.POST['subject'],
            qualification=request.POST.get('qualification', ''),
            experience=request.POST.get('experience', 0),
            teacher_id=request.POST['teacher_id'],
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            pincode=request.POST.get('pincode', ''),
            profile_picture=request.FILES.get('profile_picture'),
            password=request.POST['password'],
            std=request.POST.get('std'),
            division=request.POST.get('division'),
            is_approved=False  # Explicitly set approval to False initially
        )
        return redirect('login')
    return render(request, 'Teacher/register.html', {
        'grades': grades,
        'divisions': divisions
    })

def upload_diary(request):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        Diary.objects.create(
            teacher=teacher,
            title=request.POST['title'],
            content=request.POST['content'],
            file=request.FILES.get('file'),
            is_approved=False
            
        )
        messages.success(request, "Diary uploaded successfully!")
        return redirect('upload_diary')
    return render(request, 'Teacher/diary.html')


def post_alert(request):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        Alert.objects.create(
            teacher=teacher,
            title=request.POST['title'],
            message=request.POST['message'],
            is_approved=False
        )
        messages.success(request, "Alert posted successfully!")
        return redirect('post_alert')
    return render(request, 'Teacher/alerts.html')


def update_performance(request):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        Performance.objects.create(
            teacher=teacher,
            student_name=request.POST['student_name'],
            subject=request.POST['subject'],
            score=request.POST['score'],
            remarks=request.POST.get('remarks', ''),
            is_approved=False
        )
        messages.success(request, "Performance updated successfully!")
        return redirect('update_performance')
    students = Student.objects.all()
    return render(request, 'Teacher/performance.html', {'students': students})


def send_message(request):
    teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        message_text = request.POST.get('message')
        if student_name and message_text:
            Message.objects.create(
                teacher=teacher,
                student_name=student_name,
                message=message_text,
                is_approved=False
            )
            messages.success(request, "Message sent successfully!")
        else:
            messages.error(request, "Please fill in all fields.")
        return redirect('send_message')
    students = Student.objects.all()
    return render(request, 'Teacher/messages.html', {'students': students})


def post_event(request):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        Event.objects.create(
            teacher=teacher,
            title=request.POST['title'],
            date=request.POST['date'],
            description=request.POST['description'],
            is_approved=False
        )
        messages.success(request, "Event posted successfully!")
        return redirect('post_event')
    return render(request, 'Teacher/events.html')


def give_feedback(request):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        Feedback.objects.create(
            teacher=teacher,
            student_name=request.POST['student_name'],
            feedback=request.POST['feedback']
        )
        messages.success(request, "Feedback submitted successfully!")
        return redirect('give_feedback')
    return render(request, 'Teacher/feedback.html')


def upload_report(request):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        Report.objects.create(
            teacher=teacher,
            title=request.POST['title'],
            description=request.POST.get('description', ''),
            report_file=request.FILES['report_file'],
            is_approved=False
        )
        messages.success(request, "Report uploaded successfully!")
        return redirect('upload_report')
    return render(request, 'Teacher/reports.html')


def teacher_dashboard(request):
    return render(request, 'Teacher/dashboard.html')


def parent_records(request):
    if 'teacher_id' not in request.session:
        return redirect('login')
    parents = Parent.objects.all()
    return render(request, 'Teacher/parent_records.html', {'parents': parents})


def delete_parent(request, parent_id):
    if 'teacher_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        parent = get_object_or_404(Parent, id=parent_id)
        parent.delete()
    return redirect('parent_records')


def show_students(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')
    teacher = get_object_or_404(Teacher, id=teacher_id)
    students = Student.objects.filter(std=teacher.std)
    return render(request, 'Teacher/student_details.html', {'students': students, 'teacher': teacher})


def parent_record_by_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        parent = student.parent
    except Student.DoesNotExist:
        return HttpResponse("Student not found!", status=404)
    return render(request, 'Teacher/parent_records.html', {'parents': [parent]})


def teacher_profile(request):
    teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
    return render(request, 'Teacher/profile.html', {'teacher': teacher})


def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher_id'))
        if not check_password(old_password, teacher.password):
            messages.error(request, "Old password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            teacher.password = make_password(new_password)
            teacher.save()
            messages.success(request, "Password changed successfully.")
            return redirect('teacher_dashboard')
    return render(request, 'Teacher/change_password.html')
