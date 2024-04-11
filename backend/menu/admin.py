from django.contrib import admin

from .models import Menu


class ChildrensInline(admin.TabularInline):
    model = Menu
    extra = 2


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'href', 'parent')
    inlines = (ChildrensInline,)
    ordering = ('parent', 'name')
    list_filter = ('parent',)
