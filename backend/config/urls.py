from config import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from menu.views import menu


urlpatterns = [
    path(route='admin/', view=admin.site.urls, name='admin'),
    path(route='', view=menu, name='menu'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG is True:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
