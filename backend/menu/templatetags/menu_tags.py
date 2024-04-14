import json

from django import template
from menu.models import Menu


register = template.Library()


@register.inclusion_tag('menu/render-menu.html')
def render_menu(menu_name: str):
    menu_tree = Menu.objects.with_childrens(name=menu_name)
    return {
        'menu_tree': json.dumps(menu_tree),
        'menu_id': f'menu-{menu_tree['id']}-{menu_tree['href']}'
    }
