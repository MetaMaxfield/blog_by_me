import os
from django.http import StreamingHttpResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from dotenv import load_dotenv
from blog_by_me.settings import CURRENT_DATETIME, COUNT_POSTS_ON_PAGE
from services.blog.paginator import create_pagination
from services.blog.video_player import open_file
from services import client_ip, rating, search, validator
from .models import Post
from .forms import CommentsForm, RatingForm
from services.caching import get_cached_objects_or_queryset


load_dotenv()


# class PostsView(View):
#     """Посты блога"""
#     def get(
#             self,
#             request: HttpRequest,
#     ) -> HttpResponse:
#         object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
#         paginator, post_list = create_pagination(request, object_list)
#         return render(request, 'blog/post_list.html', {'post_list': post_list,
#                                                        'paginator': paginator})


class PostsView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
    paginate_by = COUNT_POSTS_ON_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post_list'] = context['page_obj']
        del context['page_obj']

        return context


class PostsFilterDateView(View):
    """Посты блога с фильтрацией по дате"""
    def get(
            self,
            request: HttpRequest,
            date_posts: int
    ) -> HttpResponse:
        object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        object_list = search.search_by_date(date_posts, object_list)
        paginator, post_list = create_pagination(request, object_list)
        return render(request, 'blog/post_list.html', {'post_list': post_list,
                                                       'date_posts': date_posts,
                                                       'current_datetime': CURRENT_DATETIME,
                                                       'paginator': paginator})


class PostsFilterTagView(View):
    """Посты блога с фильтрацией по тегу"""
    def get(
            self,
            request: HttpRequest,
            tag_slug: str
    ) -> HttpResponse:
        object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        tag, object_list = search.search_by_tag(tag_slug, object_list)
        paginator, post_list = create_pagination(request, object_list)
        return render(request, 'blog/post_list.html', {'post_list': post_list,
                                                       'tag': tag,
                                                       'paginator': paginator})

class PostDetailView(View):
    """Пост"""
    def get(
            self,
            request: HttpRequest,
            slug: str
    ) -> HttpResponse:
        post = get_cached_objects_or_queryset(os.getenv('KEY_POST_DETAIL'), slug)
        form = CommentsForm()
        rating_form = RatingForm()
        received_ip = client_ip.get_client_ip(request)
        selected = validator.validator_selected_rating(received_ip, post)
        return render(request, 'blog/post_detail.html',
                      {'post': post,
                       'form': form,
                       'rating_form': rating_form,
                       'selected': selected}
                      )


class CommentsView(View):
    """Комментарии"""
    def post(
             self,
             request: HttpRequest,
             pk: int
    ) -> HttpResponseRedirect:
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
    def get(
            self,
            request: HttpRequest
    ) -> HttpResponse:
        categories = get_cached_objects_or_queryset(os.getenv('KEY_CATEGORIES_LIST'))
        posts = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        return render(request, 'blog/category_list.html', {'categories': categories, 'posts': posts})


class SearchView(View):
    """Поиск"""
    def get(
            self,
            request: HttpRequest
    ) -> HttpResponse:
        q = request.GET.get('q').capitalize()
        current_language = request.LANGUAGE_CODE
        object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        object_list = search.search_by_q(q, object_list, current_language)
        paginator, post_list = create_pagination(request, object_list)
        return render(request, 'blog/post_list.html', {'post_list': post_list,
                                                       'paginator': paginator,
                                                       'q': q})


class VideosView(View):
    """Видеозаписи блога"""
    def get(
            self,
            request: HttpRequest
    ) -> HttpResponse:
        video_list = get_cached_objects_or_queryset(os.getenv('KEY_VIDEOS_LIST'))
        return render(request, 'blog/video_list.html', {'video_list': video_list})


class VideoPlayView(View):
    """Видеопроигрыватель"""
    def get(
            self,
            request: HttpRequest,
            pk: int
    ) -> StreamingHttpResponse:
        file, status_code, content_length, content_range = open_file(request, pk)
        response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(content_length)
        response['Cache-Control'] = 'no-cache'
        response['Content-Range'] = content_range
        return response


class AddRatingView(View):
    """Рейтинг"""
    def post(
            self,
            request: HttpRequest
    ) -> HttpResponse:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating.create_or_update_rating(request)
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
