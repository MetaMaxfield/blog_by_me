import os
from calendar import Calendar
from datetime import datetime
from typing import Union

from django import template
from django.db.models import QuerySet

from blog_by_me.settings import CURRENT_DATETIME
from services.caching import get_cached_objects_or_queryset
from services.template_tags import add_posts_days_in_list

register = template.Library()


@register.inclusion_tag('include/tags/top_posts.html')
def top_posts() -> dict[str, QuerySet]:
    """
    Шаблонный тег, отображающий популярные посты блога в зависимости от рейтинга
    """
    top_list = get_cached_objects_or_queryset(os.getenv('KEY_TOP_POSTS'))
    return {'top_list': top_list}


@register.inclusion_tag('include/tags/last_posts.html')
def last_posts() -> dict[str, QuerySet]:
    """
    Шаблонный тег, отображающий последние добавленные посты в блоге
    """
    last_posts = get_cached_objects_or_queryset(os.getenv('KEY_LAST_POSTS'))
    return {'last_posts': last_posts}


@register.inclusion_tag('include/tags/all_tags.html')
def all_tags() -> dict[str, QuerySet]:
    """
    Шаблонный тег, отображающий все теги постов в блоге и их количество
    """
    all_tags = get_cached_objects_or_queryset(os.getenv('KEY_ALL_TAGS'))
    return {'all_tags': all_tags}


@register.inclusion_tag('include/tags/calendar.html')
def calendar() -> dict[str, Union[list[list[int]]], datetime, set]:
    """
    Шаблонный тег, отображающий календарь
    """
    qs_calendar = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_CALENDAR'))
    return {
        'month': Calendar().monthdayscalendar(CURRENT_DATETIME.year, CURRENT_DATETIME.month),
        'current_datetime': CURRENT_DATETIME,
        'posts_days': add_posts_days_in_list(qs_calendar),
    }
