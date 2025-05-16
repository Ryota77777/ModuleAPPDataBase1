from django.contrib import admin
from .models import ModuleRecord

@admin.register(ModuleRecord)
class ModuleRecordAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'date', 'revenue', 'expenses', 'profit')
    list_filter = ('company_name', 'date')
    search_fields = ('company_name',)

admin.site.site_header = "Управление табельным учетом специалиста"
admin.site.index_title = "Администрирование данных"
