from __future__ import annotations

import json

from django import http
from django.shortcuts import render
from menu.models import Menu


def menu(request: http.HttpRequest) -> http.HttpResponse:
    context = {'menu_items': json.dumps([Menu.objects.with_childrens(19)])}
    return render(request, 'menu.html', context)
