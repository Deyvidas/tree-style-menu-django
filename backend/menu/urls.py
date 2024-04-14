from django.urls import path

from .views import menu


urlpatterns = [
    path(route='', view=menu, name='menu'),
]
