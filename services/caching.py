from typing import Union

from django.core.cache import cache
from django.db.models import QuerySet

from blog_by_me.settings import CACHE_KEY, CACHE_TIMES, T
from services.queryset import qs_definition


def _get_cache_time(qs_key: str) -> int:
    """Получение времени кэширования в зависимости от типа данных"""
    return CACHE_TIMES.get(qs_key, 300)


def get_cached_objects_or_queryset(qs_key: str, slug_or_pk: Union[str, int] = '') -> Union[QuerySet, T]:
    """Получения кэша или вызов QS"""
    object_list_or_object = cache.get(f'{CACHE_KEY}{qs_key}{slug_or_pk}')
    if not object_list_or_object:
        object_list_or_object = qs_definition(qs_key, slug_or_pk)
        cache_time = _get_cache_time(qs_key)
        cache.set(f'{CACHE_KEY}{qs_key}{slug_or_pk}', object_list_or_object, cache_time)
    return object_list_or_object
