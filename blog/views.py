import os
from django.http import StreamingHttpResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
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


# class PostsFilterDateView(View):
#     """Посты блога с фильтрацией по дате"""
#     def get(
#             self,
#             request: HttpRequest,
#             date_posts: int
#     ) -> HttpResponse:
#         object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
#         object_list = search.search_by_date(date_posts, object_list)
#         paginator, post_list = create_pagination(request, object_list)
#         return render(request, 'blog/post_list.html', {'post_list': post_list,
#                                                        'date_posts': date_posts,
#                                                        'current_datetime': CURRENT_DATETIME,
#                                                        'paginator': paginator})


class PostsFilterDateView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
    paginate_by = COUNT_POSTS_ON_PAGE

    def get_queryset(self):
        queryset = super().get_queryset()
        return search.search_by_date(self.kwargs['date_posts'], queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_datetime'] = CURRENT_DATETIME
        context['date_posts'] = self.kwargs['date_posts']

        context['post_list'] = context['page_obj']
        del context['page_obj']

        return context


# class PostsFilterTagView(View):
#     """Посты блога с фильтрацией по тегу"""
#     def get(
#             self,
#             request: HttpRequest,
#             tag_slug: str
#     ) -> HttpResponse:
#         object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
#         tag, object_list = search.search_by_tag(tag_slug, object_list)
#         paginator, post_list = create_pagination(request, object_list)
#         return render(request, 'blog/post_list.html', {'post_list': post_list,
#                                                        'tag': tag,
#                                                        'paginator': paginator})


class PostsFilterTagView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
    paginate_by = COUNT_POSTS_ON_PAGE

    def get_queryset(self):
        queryset = super().get_queryset()
        tag, queryset = search.search_by_tag(self.kwargs['tag_slug'], queryset)
        self.kwargs['tag'] = tag
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tag'] = self.kwargs['tag']

        context['post_list'] = context['page_obj']
        del context['page_obj']

        return context


# class PostDetailView(View):
#     """Пост"""
#     def get(
#             self,
#             request: HttpRequest,
#             slug: str
#     ) -> HttpResponse:
#         post = get_cached_objects_or_queryset(os.getenv('KEY_POST_DETAIL'), slug)
#         selected = validator.validator_selected_rating(client_ip.get_client_ip(request), post)
#         return render(request, 'blog/post_detail.html',
#                       {'post': post,
#                        'form': CommentsForm(),
#                        'rating_form': RatingForm(),
#                        'selected': selected})


class PostDetailView(DetailView):
    def get_object(self, **kwargs):
        return get_cached_objects_or_queryset(os.getenv('KEY_POST_DETAIL'), self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['rating_form'] = RatingForm
        context['selected'] = validator.validator_selected_rating(
            client_ip.get_client_ip(self.request), context['post']
        )
        return context


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


# class CategoryView(View):
#     """Категории"""
#     def get(
#             self,
#             request: HttpRequest
#     ) -> HttpResponse:
#         categories = get_cached_objects_or_queryset(os.getenv('KEY_CATEGORIES_LIST'))
#         posts = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
#         return render(request, 'blog/category_list.html', {'categories': categories, 'posts': posts})


class CategoryView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_CATEGORIES_LIST'))
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
        return context


# class SearchView(View):
#     """Поиск"""
#     def get(
#             self,
#             request: HttpRequest
#     ) -> HttpResponse:
#         q = request.GET.get('q')
#         current_language = request.LANGUAGE_CODE
#         object_list = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
#         object_list = search.search_by_q(q, object_list, current_language)
#         paginator, post_list = create_pagination(request, object_list)
#         return render(request, 'blog/post_list.html', {'post_list': post_list,
#                                                        'paginator': paginator,
#                                                        'q': q})


class SearchView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_POSTS_LIST'))
    paginate_by = COUNT_POSTS_ON_PAGE

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = super().get_queryset()
        self.kwargs['q'] = q
        current_language = self.request.LANGUAGE_CODE
        return search.search_by_q(q, queryset, current_language)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['q'] = self.kwargs['q']

        context['post_list'] = context['page_obj']
        del context['page_obj']

        return context


# class VideosView(View):
#     """Видеозаписи блога"""
#     def get(
#             self,
#             request: HttpRequest
#     ) -> HttpResponse:
#         video_list = get_cached_objects_or_queryset(os.getenv('KEY_VIDEOS_LIST'))
#         return render(request, 'blog/video_list.html', {'video_list': video_list})


class VideosView(ListView):
    queryset = get_cached_objects_or_queryset(os.getenv('KEY_VIDEOS_LIST'))


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
