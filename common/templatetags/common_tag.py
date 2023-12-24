from django import template
from services import template_tags


register = template.Library()


@register.filter
def ru_plural(value, variants):
    """
    Шаблонный фильтр для изменения окончания слова в зависимости от количества
    (Русскоязычный аналог "pluralize")
    """
    return template_tags.service_ru_plural(value, variants)


@register.filter
def share_url_format(url):
    """
    Шаблонный фильтр для форматирования URL адреса для блока "Поделиться"
    """
    return template_tags.service_share_url_format(url)
