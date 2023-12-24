from django import template


register = template.Library()


@register.inclusion_tag('include/tags/breadcrumbs/breadcrumb_home.html')
def breadcrumb_home(url='/', title=''):
    """ Корневая страница навигационной цепочки """
    return {
        'url': url,
        'title': title
    }


@register.inclusion_tag('include/tags/breadcrumbs/breadcrumb_item.html')
def breadcrumb_item(url, title, position):
    """ Промежуточная страница навигационной цепочки """
    return {
        'url': url,
        'title': title,
        'position': position
    }


@register.inclusion_tag('include/tags/breadcrumbs/breadcrumb_active.html')
def breadcrumb_active(url, title, position):
    """ Активная страница навигационной цепочки """
    return {
        'url': url,
        'title': title,
        'position': position
    }
