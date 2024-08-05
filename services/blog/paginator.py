from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest

from blog_by_me.settings import COUNT_POSTS_ON_PAGE


def create_pagination(request: HttpRequest, object_list: QuerySet) -> tuple[Paginator, QuerySet]:
    paginator = Paginator(object_list, COUNT_POSTS_ON_PAGE)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    return paginator, object_list
