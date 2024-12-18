# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render
# from django.views import View
from django.views.generic import DetailView, ListView

from blog_by_me.settings import KEY_AUTHOR_DETAIL, KEY_AUTHORS_LIST
from services.caching import get_cached_objects_or_queryset

# class AuthorsView(View):
#     """Список пользователей"""
#     def get(
#             self,
#             request: HttpRequest
#     ) -> HttpResponse:
#         authors = get_cached_objects_or_queryset(KEY_AUTHORS_LIST)
#         return render(request, 'users/author_list.html', {'authors': authors})


class AuthorsView(ListView):
    """Список пользователей"""

    context_object_name = 'authors'
    template_name = 'users/author_list.html'

    def get_queryset(self):
        return get_cached_objects_or_queryset(KEY_AUTHORS_LIST)


# class AuthorDetailView(View):
#     """Профиль пользователя"""
#     def get(
#             self,
#             request: HttpRequest,
#             pk: int
#     ) -> HttpResponse:
#         user = get_cached_objects_or_queryset(KEY_AUTHOR_DETAIL, pk)
#         return render(request, 'users/author_detail.html', {'author': user})


class AuthorDetailView(DetailView):
    """Профиль пользователя"""

    context_object_name = 'author'
    template_name = 'users/author_detail.html'

    def get_object(self, **kwargs):
        return get_cached_objects_or_queryset(KEY_AUTHOR_DETAIL, self.kwargs['pk'])
