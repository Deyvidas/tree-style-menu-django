from __future__ import annotations

from typing import Self
from typing import TypedDict

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.forms import model_to_dict
from slugify import slugify


NAME_MAX_LENGTH = 30
HREF_MAX_LENGTH = 30

CACHE_TIMEOUT_SEC = 60 * 5
MENU_QS_CACHE_KEY = 'menu_qs'


type TQS = models.QuerySet['Menu']


class TMenuItem(TypedDict):
    id: int
    name: str
    href: str
    parent: int | None
    childs: list[TMenuItem]


class MenuManger(models.Manager):
    def get_queryset(self) -> TQS:
        return self.get_cached_menu()

    def with_childrens(self, parent_id) -> TMenuItem:
        menu_set = [TMenuItem(**model_to_dict(i)) for i in self.all()]
        return self._get_tree(parent_id, menu_set)

    def _get_tree(self, parent_id: int, menu: list[TMenuItem]) -> TMenuItem:
        parent = list(filter(lambda i: i['id'] == parent_id, menu))[0]
        childs = list(filter(lambda i: i['parent'] == parent_id, menu))
        parent['childs'] = [self._get_tree(c['id'], menu) for c in childs]
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


class Menu(models.Model):
    objects: MenuManger = MenuManger()

    name = models.CharField(
        verbose_name='link name',
        max_length=NAME_MAX_LENGTH,
    )
    href = models.CharField(
        verbose_name='link suffix',
        blank=True,
        max_length=HREF_MAX_LENGTH,
    )
    parent = models.ForeignKey(
        to='self',
        related_name='childrens',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    childrens: models.Manager[Self]

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        fields = ('id', 'name', 'href')
        return f'{self.__class__.__name__}({model_to_dict(self, fields)})'


def menu_pre_save(instance: Menu, *args, **kwargs):
    if not instance.href:
        instance.href = slugify(instance.name, max_length=HREF_MAX_LENGTH)


pre_save.connect(receiver=menu_pre_save, sender=Menu)


def menu_post_save(sender: Menu, *args, **kwargs):
    sender.objects.actualize_cached_menu()


post_save.connect(receiver=menu_post_save, sender=Menu)


def menu_post_delete(instance: Menu, *args, **kwargs):
    instance._meta.model.objects.actualize_cached_menu()


post_delete.connect(receiver=menu_post_delete, sender=Menu)
