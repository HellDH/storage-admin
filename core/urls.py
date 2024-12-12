from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static
from main.admin import admin_site

urlpatterns = [
    path('', views.index),
    path('admin/', admin_site.urls),
    path('admin/inventory/', views.InventPageView.as_view(), name='inventory_page')    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
