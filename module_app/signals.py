from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EmployeeProfile, AttendanceLog, MonthlyReport
from datetime import datetime

print("Сигналы загружены")  # ← для отладки

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'employeeprofile'):
            instance.employeeprofile.save()

@receiver(post_save, sender=AttendanceLog)
def update_monthly_report(sender, instance, **kwargs):
    employee = instance.employee
    log_date = instance.date
    month_str = log_date.strftime('%B %Y')

    logs = AttendanceLog.objects.filter(
        employee=employee,
        date__year=log_date.year,
        date__month=log_date.month
    )

    total_hours = sum(log.hours for log in logs)
    overtime_hours = max(0, total_hours - 160)

    report, created = MonthlyReport.objects.get_or_create(
        employee=employee,
        month=month_str
    )
    report.total_hours = round(total_hours, 2)
    report.overtime_hours = round(overtime_hours, 2)
    report.save()


