from typing import Tuple, Optional
from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from blog_by_me.settings import CURRENT_DATETIME


def search_by_date_or_tag(
        date_posts: int | None,
        tag_slug: str | None,
        object_list: QuerySet
) -> Tuple[Optional[Tag], QuerySet]:
    """
    Функция валидирует записи по тегу или дате,
    а также возвращает текущую дату
    """
    tag = None
    if date_posts:
        object_list = object_list.filter(
            created__year=CURRENT_DATETIME.year,
            created__month=CURRENT_DATETIME.month,
            created__day=date_posts,
        )
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    return tag, object_list


def search_by_q(
        q: str,
        object_list: QuerySet,
        current_language: str
) -> QuerySet:
    """
    Поиск по названию и содержанию в зависимости от выбранного языка,
    сортировка результатов поиска с использованием специальных классов для PostgeSQL
    """
    if current_language == 'ru':
        search_vector = SearchVector('title_ru', 'body_ru')
    else:
        search_vector = SearchVector('title_en', 'body_en')
    search_query = SearchQuery(q)
    object_list = object_list.annotate(
        search=search_vector, rank=SearchRank(search_vector, search_query)
    ).filter(
        search=search_query, draft=False
    ).order_by('-rank')
    return object_list
