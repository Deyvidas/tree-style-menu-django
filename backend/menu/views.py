from __future__ import annotations

import json
from typing import TypedDict

from django import http
from django.core.cache import cache
from django.shortcuts import render
from menu.models import Menu


def menu(request: http.HttpRequest) -> http.HttpResponse:
    query_set = cache.get('query_set')
    if query_set is None:
        query_set = list(map(lambda i: TItem(**i), Menu.objects.values()))
        cache.set('query_set', query_set)

    res = get_childrens(19, query_set)
    return render(request, 'menu.html', {'menu_items': json.dumps([res])})


class TItem(TypedDict):
    id: int
    name: str
    href: str
    parent_id: int | None
    childs: list[TItem]


def get_childrens(parent_id: int | None, query_set: list[TItem]) -> TItem:
    parent = list(filter(lambda i: i['id'] == parent_id, query_set))[0]
    childs = list(filter(lambda i: i['parent_id'] == parent_id, query_set))
    parent['childs'] = [get_childrens(c['id'], query_set) for c in childs]

    return parent
