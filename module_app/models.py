from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class ModuleRecord(models.Model):
    company_name = models.CharField(max_length=255)
    date = models.DateField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    expenses = models.DecimalField(max_digits=15, decimal_places=2)
    profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.profit = self.revenue - self.expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name} ({self.date})"

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.position or 'Сотрудник'}"

    @property
    def total_hours(self):
        return round(self.attendance_logs.aggregate(models.Sum('hours'))['hours__sum'] or 0, 2)

class WorkSchedule(models.Model):
    DAY_CHOICES = [
        ('Пн', 'Понедельник'), ('Вт', 'Вторник'), ('Ср', 'Среда'),
        ('Чт', 'Четверг'), ('Пт', 'Пятница'), ('Сб', 'Суббота'), ('Вс', 'Воскресенье')
    ]
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=2, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.user.username} - {self.get_day_display()}"

class AttendanceLog(models.Model):
    EVENT_TYPES = [
        ('start', 'Начало работы'),
        ('break', 'Перерыв'),
        ('resume', 'Продолжение работы'),
        ('end', 'Окончание работы'),
    ]
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='attendance_logs')
    date = models.DateField()
    time = models.TimeField()
    event = models.CharField(max_length=10, choices=EVENT_TYPES)
    hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date} - {self.get_event_display()}"

class MonthlyReport(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='monthly_reports')
    month = models.CharField(max_length=20)  # напр., "Май 2025"
    total_hours = models.FloatField(default=0)
    overtime_hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee.user.username} - {self.month}"


