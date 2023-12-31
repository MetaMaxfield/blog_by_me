import os
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from dotenv import load_dotenv
from blog_by_me.settings import CURRENT_DATETIME
from services.blog.paginator import create_pagination
from services.blog.video_player import open_file
from services.client_ip import get_client_ip
from services.rating import create_or_update_rating
from services import search
from services.validator import validator_selected_rating
from .models import Post
from .forms import CommentsForm, RatingForm
from services.caching import get_cached_objects_or_queryset


load_dotenv()


class PostsView(View):
    """Посты блога"""
    def get(self, request, date_posts=None, tag_slug=None):
        object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        tag, object_list = search.search_by_date_or_tag(date_posts, tag_slug, object_list)
        paginator, page, post_list = create_pagination(request, object_list)
        return render(request, 'blog/post_list.html', {'page': page,
                                                       'post_list': post_list,
                                                       'tag': tag,
                                                       'date_posts': date_posts,
                                                       'current_datetime': CURRENT_DATETIME,
                                                       'paginator': paginator})


class PostDetailView(View):
    """Пост"""
    def get(self, request, slug):
        post = get_cached_objects_or_queryset(os.getenv('KEY_POST_DETAIL'), slug)
        form = CommentsForm()
        rating_form = RatingForm()
        received_ip = get_client_ip(request)
        selected = validator_selected_rating(received_ip, post)
        return render(request, 'blog/post_detail.html',
                      {'post': post,
                       'form': form,
                       'rating_form': rating_form,
                       'selected': selected}
                      )


class CommentsView(View):
    """Комментарии"""
    def post(self, request, pk):
        form = CommentsForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())


class CategoryView(View):
    """Категории"""
    def get(self, request):
        categories = get_cached_objects_or_queryset(os.getenv('KEY_CATEGORIES_LIST'))
        posts = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        return render(request, 'blog/category_list.html', {'categories': categories, 'posts': posts})


class SearchView(View):
    """Поиск"""
    def get(self, request):
        q = request.GET.get('q').capitalize()
        current_language = request.LANGUAGE_CODE
        object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        object_list = search.search_by_q(q, object_list, current_language)
        paginator, page, post_list = create_pagination(request, object_list)
        return render(request, 'blog/post_list.html', {'page': page,
                                                       'post_list': post_list,
                                                       'paginator': paginator,
                                                       'q': q})


class VideosView(View):
    """Видеозаписи блога"""
    def get(self, request):
        video_list = get_cached_objects_or_queryset(os.getenv('KEY_VIDEOS_LIST'))
        return render(request, 'blog/video_list.html', {'video_list': video_list})


class VideoPlayView(View):
    """Видеопроигрыватель"""
    def get(self, request, pk: int):
        file, status_code, content_length, content_range = open_file(request, pk)
        response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(content_length)
        response['Cache-Control'] = 'no-cache'
        response['Content-Range'] = content_range
        return response


class AddRatingView(View):
    """Рейтинг"""
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            create_or_update_rating(request)
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
