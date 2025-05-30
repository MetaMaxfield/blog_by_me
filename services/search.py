from typing import Tuple

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from taggit.models import Tag

from blog_by_me.settings import LANGUAGES


def search_by_tag(tag_slug: str, object_list: QuerySet) -> Tuple[Tag, QuerySet]:
    """
    Функция валидирует записи по тегу,
    а также возвращает заданный тег
    """
    tag = get_object_or_404(Tag, slug=tag_slug)
    object_list = object_list.filter(tags__in=[tag])
    return tag, object_list


def search_by_date(date_posts: int, object_list: QuerySet) -> QuerySet:
    """
    Функция валидирует записи по дате
    """
    current_datetime = timezone.now()
    object_list = object_list.filter(
        publish__year=current_datetime.year,
        publish__month=current_datetime.month,
        publish__day=date_posts,
    )
    return object_list


def search_by_q(q: str, object_list: QuerySet, current_language: str) -> QuerySet:
    """
    Поиск по названию и содержанию в зависимости от выбранного языка,
    сортировка результатов поиска с использованием специальных классов для PostgeSQL
    """
    if current_language == LANGUAGES[0][0]:
        search_vector = SearchVector('title_ru', 'body_ru')
    else:
        search_vector = SearchVector('title_en', 'body_en')
    search_query = SearchQuery(q)
    object_list = (
        object_list.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
        .filter(search=search_query, draft=False)
        .order_by('-rank')
    )
    return object_list
