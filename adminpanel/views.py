from django.shortcuts import render, get_object_or_404, redirect
from Home.models import*
from Teacher.models import Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from Home.views import*

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials'})

    return render(request, 'adminpanel/login.html')


from Teacher.models import Diary, Alert, Performance, Message, Event, Report
from django.shortcuts import get_object_or_404, redirect

@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_record(request, model_name, record_id):
    models_map = {
        'student': Student,
        'teacher': Teacher,
        'parent': Parent,
        'diary': Diary,
        'alert': Alert,
        'performance': Performance,
        'message': Message,
        'event': Event,
        'report': Report,
    }
    model = models_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')

    record = get_object_or_404(model, id=record_id)
    if hasattr(record, 'is_approved'):
        record.is_approved = True
        record.save()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_record(request, model_name, record_id):
    models_map = {
        'student': Student,
        'teacher': Teacher,
        'parent': Parent,
        'diary': Diary,
        'alert': Alert,
        'performance': Performance,
        'message': Message,
        'event': Event,
        'report': Report,
    }
    model = models_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')
    record = get_object_or_404(model, id=record_id)
    record.delete()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    class_filter = request.GET.get('class')
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    parents = Parent.objects.all()

    # New: fetch all objects for admin actions
    diaries = Diary.objects.all()
    alerts = Alert.objects.all()
    performances = Performance.objects.all()
    messages = Message.objects.all()
    events = Event.objects.all()
    reports = Report.objects.all()

    if class_filter:
        students = students.filter(std=class_filter)
        teachers = teachers.filter(std=class_filter)
        parents = parents.filter(students__std=class_filter).distinct()
        diaries = diaries.filter(teacher__std=class_filter)
        alerts = alerts.filter(teacher__std=class_filter)
        performances = performances.filter(teacher__std=class_filter)
        messages = messages.filter(teacher__std=class_filter)
        events = events.filter(teacher__std=class_filter)
        reports = reports.filter(teacher__std=class_filter)

    classes = Student.objects.order_by('std').values_list('std', flat=True).distinct()
    context = {
        'students': students,
        'teachers': teachers,
        'parents': parents,
        'diaries': diaries,
        'alerts': alerts,
        'performances': performances,
        'messages': messages,
        'events': events,
        'reports': reports,
        'classes': classes,
        'selected_class': class_filter,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_registration(request, model_name, record_id):
    model_map = {
        'student': Student,
        'teacher': Teacher,
        'parent': Parent,
    }
    model = model_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')
    record = get_object_or_404(model, id=record_id)
    record.is_approved = True
    record.save()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_registration(request, model_name, record_id):
    model_map = {
        'student': Student,
        'teacher': Teacher,
        'parent': Parent,
    }
    model = model_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')
    record = get_object_or_404(model, id=record_id)
    record.delete()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_logout(request):
    auth_logout(request)
    return redirect('admin_login')

@login_required
def admin_dashboard(request):
    class_filter = request.GET.get('class')
    
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    parents = Parent.objects.all()
    
    if class_filter:
        students = students.filter(std=class_filter)
        teachers = teachers.filter(std=class_filter)
        # For parents, no class typically, but you can filter those whose students are in that class:
        parents = parents.filter(students__std=class_filter).distinct()
    
    classes = Student.objects.order_by('std').values_list('std', flat=True).distinct()
    
    context = {
        'students': students,
        'teachers': teachers,
        'parents': parents,
        'classes': classes,
        'selected_class': class_filter,
    }
    return render(request, 'adminpanel/dashboard.html', context)


def approve_registration(request, model_name, record_id):
    model_map = {
        'student': Student,
        'teacher': Teacher,
        'parent': Parent,
    }
    model = model_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')
    record = get_object_or_404(model, id=record_id)
    record.is_approved = True
    record.save()
    return redirect('admin_dashboard')


def delete_registration(request, model_name, record_id):
    model_map = {
        'student': Student,
        'teacher': Teacher,
        'parent': Parent,
    }
    model = model_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')
    record = get_object_or_404(model, id=record_id)
    record.delete()
    return redirect('admin_dashboard')
