from django.core.paginator import Paginator


def create_pagination(request, object_list):
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)
    return [paginator, page, object_list]
