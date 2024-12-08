from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.template.response import TemplateResponse

from main import models

@admin.register(LogEntry)
class LoggingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LogEntry._meta.get_fields()]
    list_filter = ('action_time',)
    list_per_page=50

@admin.register(models.Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Supply._meta.fields]
    list_filter = ('agent_id', 'count')
    list_per_page=50

@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Agent._meta.fields]
    list_filter = ('type',)
    list_per_page=50

@admin.register(models.Stack)
class StackAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Stack._meta.fields] 
    list_per_page=50

@admin.register(models.Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Cell._meta.fields] + ['is_filled']
    list_filter = ('location',)
    readonly_fields = ('is_filled',)
    list_per_page=50

