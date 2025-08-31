from django.contrib import admin
from django.urls import path, include
from Home.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='Home'),
    path('home/', home, name='Home'),
    path('index.html', home, name='Home'),
    path('register.html', register_user, name='register_user'),
    path('login.html', Login, name='login'),
    path('dashboard.html', dashboard, name='dashboard'),
    path('diary.html', diary, name='diary'),
    path('alerts.html', alerts, name='alerts'),
    path('performance.html', performance, name='performance'),
    path('messages.html', messages, name='messages'),
    path('delete/<int:student_id>/', delete_student, name='delete_student'),
    path('register_parent/', register_parent, name='register_parent'),
    path('set-language/', set_language, name='set_language'),
    path('student/profile/', student_profile, name='student_profile'),
    path('student/profile/edit/', edit_profile, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('chat/', mental_health_chat, name='mental_health_chat'),
    path('daily_study_tip/', daily_study_tip, name='daily_study_tip'),
    path('Teacher/', include('Teacher.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
