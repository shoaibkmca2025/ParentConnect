from django.contrib import admin
from .models import Parent

class ParentAdmin(admin.ModelAdmin):  # ✅ Proper base class
    list_display = ['id', 'name', 'email']  # optional

admin.site.register(Parent, ParentAdmin)
