from django.urls import path
from . import views
from Home.views import Login
urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<str:model_name>/<int:record_id>/', views.approve_registration, name='approve_registration'),
    path('delete/<str:model_name>/<int:record_id>/', views.delete_registration, name='delete_registration'),
    path('approve/<str:model_name>/<int:record_id>/', views.approve_record, name='approve_record'),
    path('delete/<str:model_name>/<int:record_id>/', views.delete_record, name='delete_record'),

]
