from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from backend.config import settings
from backend.index import index
from backend.menu import menu


urlpatterns = [
    path(route='admin/', view=admin.site.urls, name='admin'),
    path(route='', view=index, name='index'),
    path(route='menu/', view=menu, name='menu'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
