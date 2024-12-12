from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin import register
from django.contrib.admin.models import LogEntry

from django.template.response import TemplateResponse

from django.urls import reverse
from django.urls import path
from django.utils.html import format_html

from main import models, views

class CustomAdminSite(admin.AdminSite):
    # Переопределение метода get_app_list для добавление новых ссылок в главное меню
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        app_list.append({
            'name': 'Операции',
            'app_label': app_label,
            'models': [
                {
                    'name': 'Инвентаризация',
                    'object_name': 'inventorization',
                    'admin_url': reverse('inventory_page'),
                    'add_url': None,
                    'view_only': True,
                },
                {
                    'name': 'Графики',
                    'object_name': 'graphs',
                    'admin_url': reverse('graph_page'),
                    'add_url': None,
                    'view_only': True,
                },
            ]
        })
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('inventory/', self.admin_view(views.InventPageView.as_view()), name='inventory_page'),
            path('graph/', self.admin_view(views.AnalysisPageView.as_view()), name='graph_page')
        ]
        return custom_urls + urls

admin_site = CustomAdminSite()

@register(LogEntry, site=admin_site)
class LoggingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LogEntry._meta.get_fields()]
    list_filter = ('action_time', 'user_id')
    list_per_page=50

@register(models.Supply, site=admin_site)
class SupplyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Supply._meta.fields]
    list_filter = ('agent_id', 'count', 'item_price', 'name')
    list_per_page=50

@register(models.Agent, site=admin_site)
class AgentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Agent._meta.fields]
    list_filter = ('type',)
    list_per_page=50

@register(models.Stack, site=admin_site)
class StackAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Stack._meta.fields] 
    list_per_page=50

@register(models.Cell, site=admin_site)
class CellAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Cell._meta.fields]
    list_filter = ('location',)
    readonly_fields = ('is_filled',)
    list_per_page=50

@register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]

@register(Group, site=admin_site)
class GroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Group._meta.fiels]

