import os
from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
from services.caching import get_cached_objects_or_queryset


load_dotenv()


class AuthorsView(View):
    def get(self, request):
        authors = get_cached_objects_or_queryset(os.getenv('KEY_AUTHORS_LIST'))
        return render(request, 'users/author_list.html', {'authors': authors})


class AuthorDetailView(View):
    def get(self, request, pk):
        user = get_cached_objects_or_queryset(os.getenv('KEY_AUTHOR_DETAIL'), pk)
        return render(request, 'users/author_detail.html', {'author': user})
    