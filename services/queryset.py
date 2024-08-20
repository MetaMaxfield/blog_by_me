import os
from typing import NoReturn, Union

from django.contrib.flatpages.models import FlatPage
from django.db.models import Count, QuerySet, Sum, Prefetch, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from taggit.models import Tag

from blog.models import Category, Post, Video
from blog_by_me.settings import CURRENT_DATETIME, T
from users.models import CustomUser

load_dotenv()


def _qs_post_list() -> QuerySet:
    """Общий QS с записями блога"""
    return (
        Post.objects.filter(draft=False)
        .select_related(
            'author',
            'category',
        )
        .prefetch_related('tagged_items__tag')
        .only(
            'url', 'body', 'author__username', 'author__id', 'publish', 'title', 'image', 'category__name', 'comments'
        )
        .annotate(ncomments=Count('comments'))
    )


def _qs_post_detail(slug: str) -> T | NoReturn:
    """Отдельная запись в блоге"""
    return get_object_or_404(
        Post.objects.filter(draft=False).select_related('author').annotate(ncomments=Count('comments')), url=slug
    )


def _qs_categories_list() -> QuerySet:
    """QS со списком категорий"""
    return Category.objects.all()


def _qs_videos_list() -> QuerySet:
    """QS со всеми видеозаписями"""
    return (
        Video.objects.filter(post_video__draft=False)
        .prefetch_related(
            'post_video__author',
            'post_video__category',
            'post_video__comments',
        )
        .annotate(ncomments=Count('post_video__comments'))
        .order_by('-create_at')
    )


def _qs_contact_flatpage() -> T | NoReturn:
    """
    Получение плоской страницы 'О нас'
    """
    return get_object_or_404(FlatPage, url='/contact/')


def _qs_author_list() -> QuerySet:
    """QS со всеми авторами"""
    return CustomUser.objects.all().only('id', 'username', 'image', 'description')


def _qs_author_detail(pk: int) -> T | NoReturn:
    """QS с отдельным автором"""
    return get_object_or_404(CustomUser.objects.prefetch_related('post_author'), id=pk)


def _qs_top_posts() -> QuerySet:
    """QS с тремя самыми популярными постами"""
    return (
        Post.objects.filter(draft=False).only('title', 'body', 'url')
        .alias(total_likes=Coalesce(Sum('rating_post__mark__value'), 0))
        .order_by('-total_likes')[:3]
    )


def _qs_last_posts() -> QuerySet:
    """QS с последними тремя добавленными постами"""
    return Post.objects.filter(draft=False).only('image', 'title', 'body', 'url')[:3]


def _qs_all_tags() -> QuerySet:
    """QS с десятью популярными тегами по количеству использования"""
    return Tag.objects.annotate(npost=Count('post_tags', filter=Q(post_tags__draft=False))).order_by('-npost')[:10]


def _qs_days_posts_in_current_month() -> QuerySet:
    """Дни публикаций в текущем месяце для календаря"""
    return Post.objects.filter(
        created__year=CURRENT_DATETIME.year, created__month=CURRENT_DATETIME.month, draft=False
    ).values_list('created__day')


def not_definite_qs(*args: tuple) -> NoReturn:
    """Вызов исключения если ключ для получения queryset не найден"""
    raise Exception('Ключ для получения queryset не найден.')


def qs_definition(qs_key: str, slug_or_pk: Union[str, int, None]) -> Union[QuerySet, T, NoReturn]:
    """Определение необходимого запроса в БД по ключу"""
    qs_keys = {
        os.getenv('KEY_POSTS_LIST'): _qs_post_list,
        os.getenv('KEY_POST_DETAIL'): _qs_post_detail,
        os.getenv('KEY_CATEGORIES_LIST'): _qs_categories_list,
        os.getenv('KEY_VIDEOS_LIST'): _qs_videos_list,
        os.getenv('KEY_CONTACT_FLATPAGE'): _qs_contact_flatpage,
        os.getenv('KEY_AUTHORS_LIST'): _qs_author_list,
        os.getenv('KEY_AUTHOR_DETAIL'): _qs_author_detail,
        os.getenv('KEY_TOP_POSTS'): _qs_top_posts,
        os.getenv('KEY_LAST_POSTS'): _qs_last_posts,
        os.getenv('KEY_ALL_TAGS'): _qs_all_tags,
        os.getenv('KEY_POSTS_CALENDAR'): _qs_days_posts_in_current_month,
    }
    definite_qs = qs_keys.get(qs_key, not_definite_qs)
    return definite_qs(slug_or_pk) if slug_or_pk else definite_qs()
