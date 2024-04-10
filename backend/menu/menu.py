from __future__ import annotations

import json
from typing import TypedDict

from django import http
from django.shortcuts import render


class Link(TypedDict):
    name: str
    to: str
    childrens: list[Link]


menu_items: list[Link] = [
    {
        'name': 'home',
        'to': '',
        'childrens': [
            {
                'name': 'colors',
                'to': 'colors',
                'childrens': [
                    {
                        'name': 'red',
                        'to': 'red',
                        'childrens': [
                            {
                                'name': 'dark',
                                'to': 'dark',
                                'childrens': [],
                            },
                            {
                                'name': 'light',
                                'to': 'light',
                                'childrens': [],
                            },
                        ],
                    },
                    {
                        'name': 'blue',
                        'to': 'blue',
                        'childrens': [],
                    },
                ],
            },
            {
                'name': 'cars',
                'to': 'cars',
                'childrens': [
                    {
                        'name': 'sport',
                        'to': 'sport',
                        'childrens': [],
                    },
                    {
                        'name': 'classic',
                        'to': 'classic',
                        'childrens': [],
                    },
                ],
            },
        ],
    },
    {
        'name': 'about',
        'to': 'about',
        'childrens': [
            {
                'name': 'our-site',
                'to': 'our-site',
                'childrens': [
                    {
                        'name': 'call-center',
                        'to': 'call-center',
                        'childrens': [],
                    },
                    {
                        'name': 'chat',
                        'to': 'chat',
                        'childrens': [],
                    },
                ],
            },
            {
                'name': 'socials',
                'to': 'socials',
                'childrens': [
                    {
                        'name': 'vk',
                        'to': 'vk',
                        'childrens': [],
                    },
                    {
                        'name': 'telegram',
                        'to': 'telegram',
                        'childrens': [],
                    },
                ],
            },
        ],
    },
    {
        'name': 'feedback',
        'to': 'feedback',
        'childrens': [],
    },
]


def menu(request: http.HttpRequest) -> http.HttpResponse:
    return render(request, 'menu.html', {'menu_items': json.dumps(menu_items)})
