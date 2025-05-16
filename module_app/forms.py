from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeProfile, WorkSchedule, AttendanceLog, MonthlyReport

# Регистрация пользователя
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


# Редактирование профиля сотрудника
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['profile_picture', 'position', 'department']
        labels = {
            'profile_picture': 'Фото профиля',
            'position': 'Должность',
            'department': 'Отдел',
        }


# Создание/редактирование графика работы
class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ['day', 'start_time', 'end_time']
        labels = {
            'day': 'День недели',
            'start_time': 'Начало работы',
            'end_time': 'Окончание работы',
        }


# Учёт посещаемости
class AttendanceLogForm(forms.ModelForm):
    class Meta:
        model = AttendanceLog
        fields = ['date', 'time', 'event']
        labels = {
            'date': 'Дата',
            'time': 'Время',
            'event': 'Событие',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
        }


# Месячный отчёт
class MonthlyReportForm(forms.ModelForm):
    class Meta:
        model = MonthlyReport
        fields = ['month', 'total_hours', 'overtime_hours']
        labels = {
            'month': 'Месяц',
            'total_hours': 'Всего часов',
            'overtime_hours': 'Переработка (часы)',
        }


