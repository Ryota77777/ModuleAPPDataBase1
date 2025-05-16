from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, EmployeeProfileForm, WorkScheduleForm, AttendanceLogForm, MonthlyReportForm
from .models import EmployeeProfile, WorkSchedule, AttendanceLog, MonthlyReport
import logging
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime


logger = logging.getLogger(__name__)

def home(request):
    if request.user.is_authenticated:
        # Если пользователь авторизован, перенаправляем его на страницу профиля
        return render(request, 'home.html', {'user': request.user})
    # Если не авторизован, просто рендерим страницу
    return render(request, 'home.html')



def user_logout(request):
    logout(request)
    return redirect('home')



def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        logger.info("POST запрос на регистрацию")

        if form.is_valid():
            logger.info("Форма регистрации прошла валидацию")
            user = form.save()

            # Проверка, существует ли профиль для пользователя
            if not EmployeeProfile.objects.filter(user=user).exists():
                EmployeeProfile.objects.create(user=user)  # создаём профиль при регистрации
                logger.info(f"Профиль для пользователя {user.username} успешно создан")
            else:
                logger.warning(f"Профиль для пользователя {user.username} уже существует")

            login(request, user)  # авторизация пользователя
            logger.info(f"Пользователь {user.username} успешно зарегистрирован и авторизован")
            return redirect('home')  # перенаправление на главную страницу

        else:
            logger.warning("Форма не прошла валидацию")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Ошибка в поле {field.label}: {error}")
                    logger.error(f"Ошибка в поле {field.label}: {error}")
    else:
        form = RegisterForm()
        logger.info("GET запрос на страницу регистрации")

    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Проверка наличия профиля
            if not EmployeeProfile.objects.filter(user=user).exists():
                messages.error(request, "Профиль не найден. Пожалуйста, создайте профиль.")
                return redirect('edit_profile')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверный логин или пароль.")
            return redirect('login')

    return render(request, 'login.html')


@login_required
def profile(request):
    # Проверка, существует ли профиль
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    total_hours = profile.total_hours

    # Пример: берём следующую смену (если есть)
    next_shift = WorkSchedule.objects.filter(employee=profile).order_by('day').first()
    next_shift_str = f"{next_shift.get_day_display()}, {next_shift.start_time}" if next_shift else "Нет данных"

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile,
        'total_hours': total_hours,
        'next_shift': next_shift_str
    })



@login_required
def work_hours_view(request):
    profile = request.user.employeeprofile
    hours = AttendanceLog.objects.filter(employee=profile).aggregate(Sum('hours'))['hours__sum'] or 0

    if request.method == 'POST':
        form = AttendanceLogForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.employee = profile
            entry.save()
            return redirect('work_hours')
    else:
        form = AttendanceLogForm()

    return render(request, 'work_hours.html', {'hours': hours, 'hours_form': form})



@login_required
def schedule_view(request):
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    schedule = WorkSchedule.objects.filter(employee=profile)

    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.employee = profile
            shift.save()
            return redirect('schedule')
    else:
        form = WorkScheduleForm()

    return render(request, 'schedule.html', {'schedule': schedule, 'schedule_form': form})






@login_required
def reports_view(request):
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    reports = MonthlyReport.objects.filter(employee=profile)

    if request.method == 'POST':
        form = MonthlyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.employee = profile
            report.save()
            return redirect('reports')
    else:
        form = MonthlyReportForm()

    return render(request, 'reports.html', {'reports': reports, 'report_form': form})



@login_required
def settings(request):
    return render(request, 'settings.html')


@login_required
def edit_profile(request):
    user = request.user
    profile, created = EmployeeProfile.objects.get_or_create(user=user)  # Если нет профиля, создаём

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        profile.position = request.POST.get('position', profile.position)
        profile.department = request.POST.get('department', profile.department)

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        messages.success(request, "Профиль успешно обновлен!")
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': user, 'profile': profile})

@login_required
def edit_schedule(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)

    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.employee = profile
            schedule.save()
            messages.success(request, 'График успешно добавлен.')
            return redirect('schedule')
    else:
        form = WorkScheduleForm()

    return render(request, 'edit_schedule.html', {'form': form})

@login_required
def attendance_log_view(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)

    if request.method == 'POST':
        form = AttendanceLogForm(request.POST)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.employee = profile

            # Получим последнее событие сотрудника на ту же дату
            last_log = AttendanceLog.objects.filter(
                employee=profile,
                date=new_log.date
            ).order_by('-time').first()

            # Расчёт часов:
            # 1. Если было начало работы и сейчас конец
            # 2. Если было возобновление после перерыва и сейчас конец
            if last_log and last_log.event in ['start', 'resume'] and new_log.event == 'end':
                start_dt = datetime.combine(last_log.date, last_log.time)
                end_dt = datetime.combine(new_log.date, new_log.time)
                delta = (end_dt - start_dt).total_seconds() / 3600
                new_log.hours = round(delta, 2)
            else:
                new_log.hours = 0

            new_log.save()
            messages.success(request, 'Событие добавлено.')
            return redirect('attendance_log')
    else:
        form = AttendanceLogForm()

    logs = AttendanceLog.objects.filter(employee=profile).order_by('-date', '-time')
    return render(request, 'attendance_log.html', {
        'attendance_form': form,
        'log_entries': logs
    })












