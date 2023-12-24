from django.db.models import F
from blog.models import Rating, Mark
from services.client_ip import get_client_ip
from users.models import CustomUser


def create_or_update_rating(request):
    """
    Добавление записи в БД с выбранной оценкой
    и увеличение счетчика лайков у автора
    """
    Rating.objects.update_or_create(
        ip=get_client_ip(request),
        post_id=int(request.POST.get('post')),
        defaults={'mark_id': int(request.POST.get("mark"))}
    )
    if int(request.POST.get('mark')) == Mark.objects.get(nomination='Лайк').id:
        like = CustomUser.objects.get(post_author=int(request.POST.get('post')))
        like.total_likes = F('total_likes') + 1
        like.save()
