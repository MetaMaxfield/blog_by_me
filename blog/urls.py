from django.urls import path

from . import views

urlpatterns = [
    # Главная страница
    path('', views.PostsView.as_view(), name='blog_list'),
    # Главная страница с фильтрацией по дате
    path('date/<int:date_posts>/', views.PostsFilterDateView.as_view(), name='blog_list_by_date'),
    # Главная страница с фильтрацией по тегу
    path('tag/<slug:tag_slug>/', views.PostsFilterTagView.as_view(), name='blog_list_by_tag'),
    # Главная страница с поиском по пользовательскому запросу
    path('search/', views.SearchView.as_view(), name='search'),
    # Страница с категориями
    path('categories/', views.CategoryView.as_view(), name='category_list'),
    # URL комментариев
    path('comment/<int:pk>/', views.CommentsView.as_view(), name='add_comment'),
    # Страница с видеозаписями
    path('videos/', views.VideosView.as_view(), name='video_list'),
    # URL видеозаписи
    path('stream/<int:pk>/', views.VideoPlayView.as_view(), name='stream'),
    # URL рейтинга
    path('add-rating/', views.AddRatingView.as_view(), name="add_rating"),
    # Страница отдельного поста блога
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
