from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'teacher_id', 'is_active')
    search_fields = ('name', 'email', 'subject', 'teacher_id')
    list_filter = ('subject', 'is_active', 'city', 'state')
