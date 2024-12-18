from typing import NoReturn, Union

from django.contrib.flatpages.models import FlatPage
from django.db.models import Count, Prefetch, Q, QuerySet, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from taggit.models import Tag

from blog.models import Category, Post, Video
from blog_by_me import settings
from users.models import CustomUser


def _qs_post_list() -> QuerySet:
    """Общий QS с записями блога"""
    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .select_related(
            'category',
        )
        .prefetch_related('tagged_items__tag', Prefetch('author', CustomUser.objects.only('username', 'id')))
        .defer('video', 'created', 'updated', 'draft')
        .annotate(ncomments=Count('comments'))
    )


def _qs_post_detail(slug: str) -> settings.T | NoReturn:
    """Отдельная запись в блоге"""
    return get_object_or_404(
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .prefetch_related(Prefetch('author', CustomUser.objects.only('id', 'username')))
        .annotate(ncomments=Count('comments')),
        url=slug,
    )


def _qs_categories_list() -> QuerySet:
    """QS со списком категорий"""
    return Category.objects.all()


def _qs_videos_list() -> QuerySet:
    """QS со всеми видеозаписями"""
    return (
        Video.objects.filter(post_video__draft=False, post_video__publish__lte=timezone.now())
        .prefetch_related(
            Prefetch('post_video__author', CustomUser.objects.only('username', 'id')),
            'post_video__category',
        )
        .annotate(ncomments=Count('post_video__comments'))
        .order_by('-create_at')
    )


def _qs_contact_flatpage() -> settings.T | NoReturn:
    """
    Получение плоской страницы 'О нас'
    """
    return get_object_or_404(FlatPage, url='/contact/')


def _qs_author_list() -> QuerySet:
    """QS со всеми авторами"""
    return CustomUser.objects.all().only('id', 'username', 'image', 'description')


def _qs_author_detail(pk: int) -> settings.T | NoReturn:
    """QS с отдельным автором"""
    return get_object_or_404(
        CustomUser.objects.annotate(
            nposts=Count('post_author', filter=Q(post_author__draft=False, post_author__publish__lte=timezone.now()))
        ),
        id=pk,
    )


def _qs_top_posts() -> QuerySet:
    """QS с тремя самыми популярными постами"""
    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .only('title', 'body', 'url')
        .alias(total_likes=Coalesce(Sum('rating_post__mark__value'), 0))
        .order_by('-total_likes')[:3]
    )


def _qs_last_posts() -> QuerySet:
    """QS с последними тремя добавленными постами"""
    return Post.objects.filter(draft=False, publish__lte=timezone.now()).only('image', 'title', 'body', 'url')[:3]


def _qs_all_tags() -> QuerySet:
    """QS с десятью популярными тегами по количеству использования"""
    return Tag.objects.annotate(
        npost=Count('post_tags', filter=Q(post_tags__draft=False, post_tags__publish__lte=timezone.now()))
    ).order_by('-npost')[:10]


def _qs_days_posts_in_current_month() -> QuerySet:
    """Дни публикаций в текущем месяце для календаря"""
    current_datetime = timezone.now()
    return Post.objects.filter(
        created__year=current_datetime.year,
        created__month=current_datetime.month,
        draft=False,
        publish__lte=timezone.now(),
    ).values_list('created__day')


def not_definite_qs(*args: tuple) -> NoReturn:
    """Вызов исключения если ключ для получения queryset не найден"""
    raise Exception('Ключ для получения queryset не найден.')


def qs_definition(qs_key: str, slug_or_pk: Union[str, int]) -> Union[QuerySet, settings.T, NoReturn]:
    """Определение необходимого запроса в БД по ключу"""
    qs_keys = {
        settings.KEY_POSTS_LIST: _qs_post_list,
        settings.KEY_POST_DETAIL: _qs_post_detail,
        settings.KEY_CATEGORIES_LIST: _qs_categories_list,
        settings.KEY_VIDEOS_LIST: _qs_videos_list,
        settings.KEY_CONTACT_FLATPAGE: _qs_contact_flatpage,
        settings.KEY_AUTHORS_LIST: _qs_author_list,
        settings.KEY_AUTHOR_DETAIL: _qs_author_detail,
        settings.KEY_TOP_POSTS: _qs_top_posts,
        settings.KEY_LAST_POSTS: _qs_last_posts,
        settings.KEY_ALL_TAGS: _qs_all_tags,
        settings.KEY_POSTS_CALENDAR: _qs_days_posts_in_current_month,
    }
    definite_qs = qs_keys.get(qs_key, not_definite_qs)
    return definite_qs(slug_or_pk) if slug_or_pk else definite_qs()
