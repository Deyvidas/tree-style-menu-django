from __future__ import annotations

from typing import Self

from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.forms import model_to_dict
from slugify import slugify

from .managers import MenuManger


NAME_MAX_LENGTH = 30
HREF_MAX_LENGTH = 30


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
