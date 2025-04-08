from django.core.files.uploadedfile import SimpleUploadedFile
from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory

from blog.models import Category, Comment, Mark, Post, Rating, Video
from tests.users.factories import CustomUserFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Развлечения'
    description = 'Описание категории'
    url = 'entertainment'


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    title = 'Рыбалка'
    description = 'Видео с большим уловом'
    file = SimpleUploadedFile("fishing.mp4", b"fake video content", content_type="video/mp4")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Sequence(lambda n: f'Как я провёл отпуск. Часть {n+1}')
    url = Sequence(lambda n: f'kak-ya-provel-otpusk{n+1}')
    author = SubFactory(CustomUserFactory)
    category = SubFactory(CategoryFactory)
    body = 'Содержание событий в отпуске'
    image = SimpleUploadedFile("fishing.jpeg", b"fake image content", content_type="image/jpeg")


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post = SubFactory(PostFactory)
    name = Faker('name')
    email = Faker('email')
    text = Faker('text', max_nb_chars=100)


class MarkFactory(DjangoModelFactory):
    class Meta:
        model = Mark

    nomination = 'Лайк'
    value = 1


class RatingFactory(DjangoModelFactory):
    class Meta:
        model = Rating

    ip = '127.0.0.1'
    mark = SubFactory(MarkFactory)
    post = SubFactory(PostFactory)
