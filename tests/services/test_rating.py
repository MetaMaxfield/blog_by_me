from unittest import mock

from django.test import RequestFactory, TestCase
from django.urls import reverse

from blog.models import Rating
from blog_by_me.settings import RU_TITLE_DISLIKE_MARK
from services.rating import create_or_update_rating, get_rating_or_none
from tests.blog.factories import MarkFactory, PostFactory, RatingFactory
from tests.users.factories import CustomUserFactory


class CreateOrUpdateRatingTest(TestCase):
    """Тестирование функции create_or_update_rating"""

    @classmethod
    def setUpTestData(cls):
        """Cоздание автора, поста и разновидностей оценок к посту (Лайк, Дизлайк)"""
        cls.author = CustomUserFactory()
        cls.post = PostFactory.create(author=cls.author)
        cls.like_mark = MarkFactory.create()
        cls.dislike_mark = MarkFactory(nomination=RU_TITLE_DISLIKE_MARK, value=-1)

    def start_create_or_update_rating_with_use_mock(self, request):
        """
        Запуск тестируемой функции create_or_update_rating с mock-ами
        для функции получения необходимых данных из кэша/БД
        """
        with mock.patch('services.rating.get_cached_objects_or_queryset') as mock_get_cached:
            mock_get_cached.side_effect = [self.post, self.author]
            create_or_update_rating(request)

    def setUp(self):
        """Установка лайка к посту"""
        request = RequestFactory().post(
            path=reverse('post_detail', kwargs={'slug': f'{self.post.url}'}),
            data={'post': self.post.id, 'author': self.author.id, 'mark': self.like_mark.id},
        )

        self.start_create_or_update_rating_with_use_mock(request)

    def test_create_object_rating(self):
        fact_mark = Rating.objects.get(post=self.post, post__author=self.author).mark
        self.assertEqual(fact_mark, self.like_mark)

    def test_update_user_total_likes(self):
        # перезагружаем объект из БД для актуализации изменений после F-выражения
        self.author.refresh_from_db()
        # получаем существующее значение счётчика лайков
        fact_total_likes = self.author.total_likes

        # Проверка №1. Обновление (+1) счётчика лайков у автора
        self.assertEqual(fact_total_likes, 1)

        # создаём запрос нового пользователя с дизлайком
        request = RequestFactory().post(
            path=reverse('post_detail', kwargs={'slug': f'{self.post.url}'}),
            data={'post': self.post.id, 'author': self.author.id, 'mark': self.dislike_mark.id},
        )
        request.META['REMOTE_ADDR'] = '203.0.113.195'  # устанавливаем другой IP, так как это другой пользователь

        self.start_create_or_update_rating_with_use_mock(request)

        # перезагружаем объект из БД для актуализации изменений после F-выражения
        self.author.refresh_from_db()

        # присваиваем старое количество лайков к ожидаемому значению
        # и получаем существующее значение счётчика лайков
        expected_total_likes = fact_total_likes
        fact_total_likes = self.author.total_likes

        # Проверка №2. При установке дизлайка счётчик лайков не изменяется
        self.assertEqual(fact_total_likes, expected_total_likes)


class GetRatingOrNoneTest(TestCase):
    """Тестирование функции get_rating_or_none"""

    def test_validator_selected_rating(self):
        # определние ip пользователя и поста для оценки
        client_ip = '127.0.0.1'
        post = PostFactory.create()

        # получение рейтинга к посту для заданного ip
        fact_rating = get_rating_or_none(client_ip, post)
        # Проверка №1. Рейтинг ещё не установлен, так как пользователь не оставлял оценку
        self.assertIsNone(fact_rating)

        # пользователь оценивает пост
        expected_rating = RatingFactory.create(post=post, ip=client_ip)

        # получение рейтинга к посту для заданного ip
        fact_rating = get_rating_or_none(client_ip, post)
        # Проверка №2. Возвращённый рейтинг совпадает с тем, что оставил пользователь
        self.assertEqual(fact_rating, expected_rating)
