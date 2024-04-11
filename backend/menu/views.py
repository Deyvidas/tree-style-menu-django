from __future__ import annotations

import json
from typing import NotRequired
from typing import Required
from typing import TypedDict

from django import http
from django.db.models import Count
from django.db.models import QuerySet
from django.shortcuts import render
from menu.models import Menu


class TMenuKwargs(TypedDict):
    name: Required[str]
    href: NotRequired[str]
    childrens: list[NotRequired[TMenuKwargs]]


def menu(request: http.HttpRequest) -> http.HttpResponse:
    parents = Menu.objects.annotate(count=Count('parent')).filter(count=0)
    res = [get_children(p) for p in parents]
    return render(request, 'menu.html', {'menu_items': json.dumps(res)})


def get_children(parent: Menu) -> TMenuKwargs:
    result: TMenuKwargs = {
        'childrens': [],
        'name': parent.name,
        'href': parent.href,
    }

    childrens: QuerySet[Menu] = getattr(parent, 'childrens')
    for children in childrens.all():
        result['childrens'].append(get_children(children))

    return result
