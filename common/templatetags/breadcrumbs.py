from typing import Union
from django import template


register = template.Library()


@register.inclusion_tag('include/tags/breadcrumbs/breadcrumb_home.html')
def breadcrumb_home(
        url: str = '/',
        title: str = ''
) -> dict[str, str]:
    """ Корневая страница навигационной цепочки """
    return {
        'url': url,
        'title': title
    }


@register.inclusion_tag('include/tags/breadcrumbs/breadcrumb_item.html')
def breadcrumb_item(
        url: str,
        title: str,
        position: int
) -> dict[str, Union[str, int]]:
    """ Промежуточная страница навигационной цепочки """
    return {
        'url': url,
        'title': title,
        'position': position
    }


@register.inclusion_tag('include/tags/breadcrumbs/breadcrumb_active.html')
def breadcrumb_active(
        url: str,
        title: str,
        position: int
) -> dict[str, Union[str, int]]:
    """ Активная страница навигационной цепочки """
    return {
        'url': url,
        'title': title,
        'position': position
    }
