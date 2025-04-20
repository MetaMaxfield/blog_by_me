from typing import Optional

from django.db.models import F
from django.http import HttpRequest

from blog.models import Mark, Rating
from blog_by_me.settings import KEY_AUTHOR_DETAIL, KEY_POST_DETAIL, RU_TITLE_LIKE_MARK, T
from services.caching import get_cached_objects_or_queryset
from services.client_ip import get_client_ip


def create_or_update_rating(request: HttpRequest) -> None:
    """
    Добавление записи в БД с выбранной оценкой
    и увеличение счетчика лайков у автора
    """
    Rating.objects.update_or_create(
        ip=get_client_ip(request),
        post=get_cached_objects_or_queryset(KEY_POST_DETAIL, request.POST.get('post')),
        defaults={'mark_id': int(request.POST.get("mark"))},
    )
    if int(request.POST.get('mark')) == Mark.objects.get(nomination_ru=RU_TITLE_LIKE_MARK).id:
        user = get_cached_objects_or_queryset(KEY_AUTHOR_DETAIL, request.POST.get('author'))
        user.total_likes = F('total_likes') + 1
        user.save()


def get_rating_or_none(received_ip: str, post: T) -> Optional[T]:
    """Определяет устанавливал ли пользователь рейтинг к посту"""
    try:
        selected = Rating.objects.get(ip=received_ip, post=post)
    except Rating.DoesNotExist:
        selected = None
    return selected
