from django.urls import path

from . import views

urlpatterns = [
    # Страница со списком пользователей
    path('', views.AuthorsView.as_view(), name='author_list'),
    # Страница пользователя
    path('<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]
