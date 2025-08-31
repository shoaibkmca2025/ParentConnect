from django.urls import path
from . import views
from Home.views import Login

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('register/', views.teacher_register, name='teacher_register'),
    path('login/', Login, name='login'),
    path('diary/', views.upload_diary, name='upload_diary'),
    path('alerts/', views.post_alert, name='post_alert'),
    path('performance/', views.update_performance, name='update_performance'),
    path('messages/', views.send_message, name='send_message'),
    path('events/', views.post_event, name='post_event'),
    path('feedback/', views.give_feedback, name='give_feedback'),
    path('reports/', views.upload_report, name='upload_report'),
    path('parent-records/', views.parent_records, name='parent_records'),
    path('delete_parent/<int:parent_id>/', views.delete_parent, name='delete_parent'),
    path('parent-records/<int:student_id>/', views.parent_record_by_student, name='parent_record_by_student'),
    path('students/', views.show_students, name='show_students'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
