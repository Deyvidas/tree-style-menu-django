from __future__ import annotations

import json
from typing import TypedDict

from django import http
from django.shortcuts import render


class Link(TypedDict):
    name: str
    childrens: list[Link]


menu_items: list[Link] = [
    {
        'name': 'link-1',
        'childrens': [
            {
                'name': 'link-1-1',
                'childrens': [
                    {
                        'name': 'link-1-1-1',
                        'childrens': [
                            {
                                'name': 'link-1-1-1-1',
                                'childrens': [],
                            },
                            {
                                'name': 'link-1-1-1-2',
                                'childrens': [],
                            },
                        ],
                    },
                    {
                        'name': 'link-1-1-2',
                        'childrens': [],
                    },
                ],
            },
            {
                'name': 'link-1-2',
                'childrens': [
                    {
                        'name': 'link-1-2-1',
                        'childrens': [],
                    },
                    {
                        'name': 'link-1-2-2',
                        'childrens': [],
                    },
                ],
            },
        ],
    },
    {
        'name': 'link-2',
        'childrens': [
            {
                'name': 'link-2-1',
                'childrens': [
                    {
                        'name': 'link-2-1-1',
                        'childrens': [],
                    },
                    {
                        'name': 'link-2-1-2',
                        'childrens': [],
                    },
                ],
            },
            {
                'name': 'link-2-2',
                'childrens': [
                    {
                        'name': 'link-2-2-1',
                        'childrens': [],
                    },
                    {
                        'name': 'link-2-2-2',
                        'childrens': [],
                    },
                ],
            },
        ],
    },
    {
        'name': 'link-3',
        'childrens': [],
    },
]


def menu(request: http.HttpRequest) -> http.HttpResponse:
    return render(request, 'menu.html', {'menu_items': json.dumps(menu_items)})
