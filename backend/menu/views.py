from __future__ import annotations

import json

from django import http
from django.shortcuts import render
from menu.models import Menu


def menu(request: http.HttpRequest) -> http.HttpResponse:
    res = Menu.objects.get(parent=None).with_childrens
    return render(request, 'menu.html', {'menu_items': json.dumps([res])})
