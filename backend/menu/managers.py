from __future__ import annotations

from typing import TYPE_CHECKING
from typing import NotRequired
from typing import Required
from typing import TypedDict
from typing import Unpack

from django.core.cache import cache
from django.db import models
from django.forms import model_to_dict


if TYPE_CHECKING:
    from .models import Menu


CACHE_TIMEOUT_SEC = 60 * 5
MENU_QS_CACHE_KEY = 'menu_qs'


type TQS = models.QuerySet[Menu]


class TMenuGetterKwargs(TypedDict):
    id: NotRequired[int]
    name: NotRequired[str]
    href: NotRequired[str]
    parent: NotRequired[int]


class TMenuItem(TMenuGetterKwargs):
    id: Required[int]
    name: Required[str]
    href: Required[str]
    parent: Required[int | None]
    childs: Required[list[TMenuItem]]


class MenuManger(models.Manager):
    def get_queryset(self) -> TQS:
        return self.get_cached_menu()

    def with_childrens(
        self,
        **filters: Unpack[TMenuGetterKwargs],
    ) -> TMenuItem:

        if not filters:
            raise TypeError('with_childrens expect at least 1 argument, got 0')

        menu_set = [TMenuItem(**model_to_dict(i)) for i in self.all()]
        return self._get_tree(menu_set, **filters)

    def _get_tree(
        self,
        menu: list[TMenuItem],
        **filters: Unpack[TMenuGetterKwargs],
    ) -> TMenuItem:

        def _filter(item: TMenuItem, **filters: Unpack[TMenuGetterKwargs]):
            return all([item[k] == v for k, v in filters.items()])

        def filter_menu(**filters: Unpack[TMenuGetterKwargs]) -> list[TMenuItem]:  # fmt: skip # noqa E501
            return list(filter(lambda i: _filter(i, **filters), menu))

        try:
            parent = filter_menu(**filters)[0]
        except IndexError:
            raise IndexError(f'Menu with {filters} not found')
        childs = filter_menu(parent=parent['id'])

        parent['childs'] = [self._get_tree(menu, id=c['id']) for c in childs]
        return parent

    def get_cached_menu(self) -> TQS:
        query_set: TQS | None = cache.get(MENU_QS_CACHE_KEY)
        if query_set is None:
            query_set = self.actualize_cached_menu()
        return query_set

    def actualize_cached_menu(self) -> TQS:
        new_query_set = super().get_queryset()
        cache.set(MENU_QS_CACHE_KEY, new_query_set, CACHE_TIMEOUT_SEC)
        return new_query_set
