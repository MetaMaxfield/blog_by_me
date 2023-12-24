from django import template
from services.template_tags import service_format_phone_num


register = template.Library()


@register.filter
def format_phone_num(num):
    """Фильтр для отображения номера телефона в шаблоне в заданном формате"""
    return service_format_phone_num(num)

