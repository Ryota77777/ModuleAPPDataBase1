from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('work_hours/', views.work_hours_view, name='work_hours'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('attendance_log/', views.attendance_log_view, name='attendance_log'),
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
