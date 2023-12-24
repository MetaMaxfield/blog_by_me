import os
from django.contrib.flatpages.models import FlatPage
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from taggit.models import Tag

from blog.models import Post, Category, Video
from blog_by_me.settings import CURRENT_DATETIME
from users.models import CustomUser


load_dotenv()


def _qs_post_list():
    """Общий QS с записями блога"""
    return Post.objects.filter(draft=False).select_related(
        'author', 'category',
    ).prefetch_related(
        'tagged_items__tag'
    ).only(
        'url', 'body', 'author__username',
        'author__id', 'publish', 'title', 'image',
        'category__name', 'comments'
    ).annotate(
            ncomments=Count('comments')
    )


def _qs_post_detail(slug):
    """Отдельная запись в блоге"""
    return get_object_or_404(Post.objects.select_related('author').annotate(
        ncomments=Count('comments')), url=slug)


def _qs_categories_list():
    """QS со списком категорий"""
    return Category.objects.all()


def _qs_videos_list():
    """QS со всеми видеозаписями"""
    return Video.objects.filter(post_video__draft=False).prefetch_related(
        'post_video__author', 'post_video__category', 'post_video__comments',
    ).annotate(ncomments=Count('post_video__comments')).order_by('-create_at')


def _qs_contact_flatpage():
    """
    Получение плоской страницы 'О нас'
    """
    return get_object_or_404(FlatPage, url='/contact/')


def _qs_author_list():
    """QS со всеми авторами"""
    return CustomUser.objects.all().only(
        'id', 'username', 'image', 'description'
    )


def _qs_author_detail(pk):
    """QS с отдельным автором"""
    return get_object_or_404(
        CustomUser.objects.prefetch_related('post_author'), id=pk
    )


def _qs_top_posts():
    """QS с тремя самыми популярными постами"""
    return Post.objects.only('title', 'body', 'rating_post', 'url').annotate(
        total_likes=Coalesce(Sum('rating_post__mark__value'), 0)
    ).order_by('-total_likes')[:3]


def _qs_last_posts():
    """QS с последними тремя добавленными постами"""
    return Post.objects.filter(draft=False).only('image', 'title', 'body', 'url')[:3]


def _qs_all_tags():
    """QS с десятью популярными тегами по количеству использования"""
    return Tag.objects.annotate(npost=Count('post_tags')).order_by('-npost')[:10]


def _qs_days_posts_in_current_month():
    """Дни публикаций в текущем месяце для календаря"""
    return Post.objects.filter(
        created__year=CURRENT_DATETIME.year,
        created__month=CURRENT_DATETIME.month,
        draft=False
    ).values_list('created__day')


def qs_definition(qs_key, slug_or_pk):
    """Определение необходимого запроса в БД по ключу"""
    if qs_key == os.getenv('KEY_POSTS_LIST'):
        return _qs_post_list()
    elif qs_key == os.getenv('KEY_POST_DETAIL'):
        return _qs_post_detail(slug_or_pk)
    elif qs_key == os.getenv('KEY_CATEGORIES_LIST'):
        return _qs_categories_list()
    elif qs_key == os.getenv('KEY_VIDEOS_LIST'):
        return _qs_videos_list()
    elif qs_key == os.getenv('KEY_CONTACT_FLATPAGE'):
        return _qs_contact_flatpage()
    elif qs_key == os.getenv('KEY_AUTHORS_LIST'):
        return _qs_author_list()
    elif qs_key == os.getenv('KEY_AUTHOR_DETAIL'):
        return _qs_author_detail(slug_or_pk)
    elif qs_key == os.getenv('KEY_TOP_POSTS'):
        return _qs_top_posts()
    elif qs_key == os.getenv('KEY_LAST_POSTS'):
        return _qs_last_posts()
    elif qs_key == os.getenv('KEY_ALL_TAGS'):
        return _qs_all_tags()
    elif qs_key == os.getenv('KEY_POSTS_CALENDAR'):
        return _qs_days_posts_in_current_month()
