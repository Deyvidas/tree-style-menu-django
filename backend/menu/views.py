from __future__ import annotations

from django import http
from django.shortcuts import render


def menu(request: http.HttpRequest) -> http.HttpResponse:
    return render(request, 'menu/index.html')
