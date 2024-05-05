import os
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from dotenv import load_dotenv
from services.caching import get_cached_objects_or_queryset


load_dotenv()


# class AuthorsView(View):
#     def get(
#             self,
#             request: HttpRequest
#     ) -> HttpResponse:
#         authors = get_cached_objects_or_queryset(os.getenv('KEY_AUTHORS_LIST'))
#         return render(request, 'users/author_list.html', {'authors': authors})


class AuthorsView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_AUTHORS_LIST'))
    context_object_name = 'authors'
    template_name = 'users/author_list.html'


class AuthorDetailView(View):
    def get(
            self,
            request: HttpRequest,
            pk: int
    ) -> HttpResponse:
        user = get_cached_objects_or_queryset(os.getenv('KEY_AUTHOR_DETAIL'), pk)
        return render(request, 'users/author_detail.html', {'author': user})
    