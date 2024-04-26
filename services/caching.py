import os
from typing import Union
from django.core.cache import cache
from django.db.models import QuerySet
from dotenv import load_dotenv
from blog_by_me.settings import T
from services.queryset import qs_definition

load_dotenv()


def get_cached_objects_or_queryset(
        qs_key: str,
        slug_or_pk: Union[str, int, None] = None
) -> Union[QuerySet, T]:
    """Получения кэша или вызов QS"""
    cache_key = os.getenv('CACHE_KEY')
    object_list_or_object = cache.get(f'{cache_key}{qs_key}{slug_or_pk}')
    if not object_list_or_object:
        object_list_or_object = qs_definition(qs_key, slug_or_pk)
        cache.set(f'{cache_key}{qs_key}{slug_or_pk}', object_list_or_object)
    return object_list_or_object
