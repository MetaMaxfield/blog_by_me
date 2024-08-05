from datetime import datetime

from django import template

from services.template_tags import service_age_tag

register = template.Library()


@register.simple_tag
def age_tag(birthday: datetime) -> int:
    """
    Простой тег, отображающий возраст пользователя
    """
    return service_age_tag(birthday)
