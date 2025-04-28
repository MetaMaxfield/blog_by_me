import math

from django.core.paginator import Paginator
from django.test import RequestFactory, TestCase
from django.urls import reverse
from parameterized import parameterized

from blog.models import Post
from blog_by_me.settings import COUNT_POSTS_ON_PAGE
from services.blog.paginator import create_pagination
from tests.blog.factories import CategoryFactory, PostFactory
from tests.users.factories import CustomUserFactory


class CreatePaginationTest(TestCase):
    """Тестирование функции create_pagination"""

    @classmethod
    def setUpTestData(cls):
        """
        Подготовка тестовых данных:
        создание постов, получение всех постов,
        создание объекта пагинатора с ожидаемыми данными
        """
        author = CustomUserFactory.create()
        category = CategoryFactory.create()
        PostFactory.create_batch(COUNT_POSTS_ON_PAGE + 2, author=author, category=category)
        cls.queryset = Post.objects.all()
        cls.expected_paginator = Paginator(cls.queryset, COUNT_POSTS_ON_PAGE)

    def test_create_pagination_paginator(self):
        # Формируем запрос для страницы блога и передаем в функцию пагинации
        request = RequestFactory().get(reverse('blog_list'))
        fact_paginator, _ = create_pagination(request, self.queryset)

        # Проверка №1. Общее количество постов в возвращаемом пагинаторе
        self.assertEqual(fact_paginator.count, COUNT_POSTS_ON_PAGE + 2)

        # Рассчитываем ожидаемое количество страниц
        expected_num_pages = math.ceil((COUNT_POSTS_ON_PAGE + 2) / COUNT_POSTS_ON_PAGE)
        # Проверка №2. Общее количество страниц в пагинаторе
        self.assertEqual(fact_paginator.num_pages, expected_num_pages)

        # Проверка №3. Количество постов на страницу в возвращаемом пагинаторе
        self.assertEqual(fact_paginator.per_page, COUNT_POSTS_ON_PAGE)

    @parameterized.expand(
        [
            # Запрос первой страницы
            ('for_first_page', '?page=1', 1),
            # Запрос без указания страницы (по умолчанию первая)
            ('for_no_page', '', 1),
            # Запрос несуществующей страницы (расчитываем номер последней страницы)
            ('for_does_not_exists', '?page=10', math.ceil((COUNT_POSTS_ON_PAGE + 2) / COUNT_POSTS_ON_PAGE)),
        ]
    )
    def test_create_pagination_object_list(self, _, page_param, expected_num_page):
        # Формируем запрос с параметром page и передаем в функцию пагинации
        request = RequestFactory().get(reverse('blog_list') + page_param)
        _, fact_paginated_queryset = create_pagination(request, self.queryset)

        # Сравниваем полученный список с ожидаемой страницей пагинатора
        self.assertQuerySetEqual(fact_paginated_queryset, self.expected_paginator.page(expected_num_page))
