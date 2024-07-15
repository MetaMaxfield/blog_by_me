from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest


def create_pagination(
        request: HttpRequest,
        object_list: QuerySet
) -> tuple[Paginator, QuerySet]:
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    return [paginator, page, object_list]
