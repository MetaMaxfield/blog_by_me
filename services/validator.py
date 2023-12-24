from blog.models import Rating


def validator_selected_rating(received_ip, post):
    """Определяет устанавливал ли пользователь рейтинг к посту"""
    try:
        selected = Rating.objects.get(ip=received_ip, post=post)
    except:
        selected = None
    return selected
