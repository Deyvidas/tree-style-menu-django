from __future__ import annotations

from typing import Self

from django.db import models
from django.db.models.signals import pre_save
from slugify import slugify


NAME_MAX_LENGTH = 30
HREF_MAX_LENGTH = 30


class Menu(models.Model):
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

    @property
    def with_childrens(self):
        return {
            'name': self.name,
            'href': self.href,
            'childrens': [c.with_childrens for c in self.childrens.all()],
        }

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        fields = ('name', 'href')
        fields = ', '.join([f'{f}: {repr(getattr(self, f))}' for f in fields])
        return f'{type(self).__name__} - ' + '{' + fields + '}'


def menu_pre_save(instance: Menu, *args, **kwargs):
    if not instance.href:
        instance.href = slugify(instance.name, max_length=HREF_MAX_LENGTH)


pre_save.connect(receiver=menu_pre_save, sender=Menu)
