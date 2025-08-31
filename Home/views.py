from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.utils import translation
from datetime import date
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import ollama  # pip install ollama
from django.contrib.auth import authenticate, login as auth_login


from .models import Student, Parent
from Teacher.models import Teacher, Diary, Alert, Performance, Message, Event, Feedback, Report


def home(request):
    return render(request, "Home/index.html")


def dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    performances = Performance.objects.filter(student_name=student.name).order_by('subject')
    subjects = [p.subject for p in performances]
    scores = [p.score for p in performances]
    context = {
        "student": student,
        "diaries": Diary.objects.all().order_by('-created_at'),
        "alerts": Alert.objects.all().order_by('-created_at'),
        "performances": performances,
        "subjects": json.dumps(subjects),
        "scores": json.dumps(scores),
        "messages": Message.objects.filter(parent_name=student.name),
        "events": Event.objects.all().order_by('-posted_at'),
        "feedbacks": Feedback.objects.filter(student_name=student.name),
        "reports": Report.objects.filter(teacher__subject__icontains=student.std),
    }
    return render(request, "Home/dashboard.html", context)
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST.get('user_type')

        if user_type == 'student':
            students = Student.objects.filter(name__iexact=username)
            if not students:
                return render(request, 'Home/login.html', {'error': 'Student not found'})
            for student in students:
                if not student.is_approved:
                    return render(request, 'Home/login.html', {'error': 'Registration not yet approved by admin'})
                if check_password(password, student.password):
                    request.session['student_id'] = student.id
                    return redirect('dashboard')
            return render(request, 'Home/login.html', {'error': 'Invalid student password'})

        elif user_type == 'teacher':
            try:
                teacher = Teacher.objects.get(name__iexact=username)
                if not teacher.is_approved:
                    return render(request, 'Home/login.html', {'error': 'Your registration is pending admin approval'})
                if check_password(password, teacher.password):
                    request.session['teacher_id'] = teacher.id
                    return redirect('teacher_dashboard')
                else:
                    return render(request, 'Home/login.html', {'error': 'Invalid teacher password'})
            except Teacher.DoesNotExist:
                return render(request, 'Home/login.html', {'error': 'Teacher not found'})

        elif user_type == 'admin':
            # Use Django's built-in authentication for admin
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                auth_login(request, user)
                # Redirect to Django admin or your custom admin dashboard
                return redirect('admin_dashboard')
            else:
                return render(request, 'Home/login.html', {'error': 'Invalid admin credentials'})

    return render(request, 'Home/login.html')

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('show_students')


def diary(request):
    diaries = Diary.objects.all().order_by('-created_at')
    return render(request, "Home/diary.html", {'diaries': diaries})


def alerts(request):
    alerts = Alert.objects.all().order_by('-created_at')
    return render(request, "Home/alerts.html", {'alerts': alerts})


def performance(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    performances = Performance.objects.filter(student_name=student.name).order_by('subject')
    subjects = [p.subject for p in performances]
    scores = [p.score for p in performances]
    context = {
        'performances': performances,
        'subjects': json.dumps(subjects),
        'scores': json.dumps(scores),
    }
    return render(request, "Home/performance.html", context)


def messages(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    teacher_messages = Message.objects.filter(parent_name=student.name).order_by('-id')
    return render(request, "Home/messages.html", {'messages': teacher_messages})


from datetime import date

def register_parent(request):
    if request.method == 'POST':
        Parent.objects.create(
            guardian_id=request.POST.get('guardian_id'),
            registration_date=date.today(),
            father_name=request.POST.get('father_name'),
            father_qualification=request.POST.get('father_qualification'),
            father_designation=request.POST.get('father_designation'),
            father_office_address=request.POST.get('father_office_address'),
            father_phone=request.POST.get('father_phone'),
            father_email=request.POST.get('father_email'),
            father_aadhaar=request.POST.get('father_aadhaar'),
            father_signature=request.POST.get('father_signature'),
            mother_name=request.POST.get('mother_name'),
            mother_qualification=request.POST.get('mother_qualification'),
            mother_designation=request.POST.get('mother_designation'),
            mother_office_address=request.POST.get('mother_office_address'),
            mother_phone=request.POST.get('mother_phone'),
            mother_email=request.POST.get('mother_email'),
            mother_aadhaar=request.POST.get('mother_aadhaar'),
            mother_signature=request.POST.get('mother_signature'),
            is_approved=False  # Explicitly set approval to False
        )
        return redirect('Home')
    return render(request, 'Home/register_parent.html')

def register_user(request):
    if request.method == 'POST':
        parent = None
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                parent = Parent.objects.get(id=parent_id)
            except Parent.DoesNotExist:
                return HttpResponse("Parent not found", status=404)
        Student.objects.create(
            name=request.POST.get('name'),
            std=request.POST.get('std'),
            division=request.POST.get('division'),
            address=request.POST.get('address'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth') or None,
            blood_group=request.POST.get('blood_group'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            father_name=request.POST.get('father_name'),
            mother_name=request.POST.get('mother_name'),
            guardian_email=request.POST.get('guardian_email'),
            guardian_phone=request.POST.get('guardian_phone'),
            admission_date=request.POST.get('admission_date') or None,
            profile_picture=request.FILES.get('profile_picture'),
            password=request.POST.get('password'),
            parent=parent,
            is_approved=False  # Explicitly set to False until admin approves
        )
        return redirect('login')
    parents = Parent.objects.order_by('father_name')
    return render(request, 'Home/register.html', {'parents': parents})

def set_language(request):
    if request.method == 'POST':
        lang_code = request.POST.get('language')
        if lang_code and lang_code in dict(settings.LANGUAGES).keys():
            request.session['django_language'] = lang_code
            translation.activate(lang_code)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def student_profile(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'Home/student_profile.html', {'student': student})


def edit_profile(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.std = request.POST.get('std')
        student.age = request.POST.get('age')
        student.address = request.POST.get('address')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth') or None
        student.blood_group = request.POST.get('blood_group')
        student.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone_number')
        student.father_name = request.POST.get('father_name')
        student.mother_name = request.POST.get('mother_name')
        student.guardian_email = request.POST.get('guardian_email')
        student.guardian_phone = request.POST.get('guardian_phone')
        student.admission_date = request.POST.get('admission_date') or None
        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
        student.save()
        return redirect('student_profile')
    return render(request, 'Home/edit_profile.html', {'student': student})


def logout_view(request):
    request.session.flush()
    return redirect('login')


@csrf_exempt
def mental_health_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        try:
            response = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "system", "content": "You are a kind, supportive mental health assistant for students. Be empathetic and positive."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response["message"]["content"]
        except Exception as e:
            print(e)
            bot_reply = "I'm here for you, but I’m having trouble connecting right now."
        return JsonResponse({"reply": bot_reply})


@csrf_exempt
def daily_study_tip(request):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": "You are an educational coach for students. Give one short, motivating daily study tip or learning insight in 2-3 sentences."},
                {"role": "user", "content": "Give me today's study tip."}
            ]
        )
        tip = response["message"]["content"]
    except Exception as e:
        print(e)
        tip = "Stay curious and consistent — even 15 minutes of focused study daily can make a big difference!"
    return JsonResponse({"tip": tip})
