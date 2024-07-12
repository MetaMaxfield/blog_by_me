from typing import Optional
from blog.models import Rating
from blog_by_me.settings import T


def validator_selected_rating(received_ip: str, post: T) -> Optional[T]:
    """Определяет устанавливал ли пользователь рейтинг к посту"""
    try:
        selected = Rating.objects.get(ip=received_ip, post=post)
    except:
        selected = None
    return selected
