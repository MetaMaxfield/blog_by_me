from django.test import TestCase
from django.utils import timezone
from parameterized import parameterized
from taggit.models import Tag

from blog.models import Post
from blog_by_me.settings import LANGUAGES
from services.search import search_by_date, search_by_q, search_by_tag
from tests.blog.factories import CategoryFactory, PostFactory
from tests.users.factories import CustomUserFactory


class SearchTest(TestCase):
    """
    Набор тестов для проверки функций фильтрации и полнотекстового поиска по постам:
    - Поиск по тегу (функция search_by_tag)
    - Поиск по дате создания поста в текущем месяце (функция search_by_date)
    - Полнотекстовый поиск по названию и содержанию в зависимости от языка (функция search_by_q)
    """

    TITLE_RU = 'Заголовок на русском'
    TITLE_EN = 'Описание на русском'
    BODY_RU = 'Title in English'
    BODY_EN = 'Body in English'

    @classmethod
    def setUpTestData(cls):
        """
        Создаёт тестовые данные:
        - Один ожидаемый пост с уникальными значениями на двух языках (ожидаемый результат поиска)
        - Три поста, не подходящие под условия поиска
        - Общий queryset всех постов сохраняется в cls.queryset
        """
        author = CustomUserFactory.create(username='Admin', email='admin@admin.com')
        category = CategoryFactory.create()
        cls.expected_post = PostFactory.create(
            title=SearchTest.TITLE_RU,
            body=SearchTest.BODY_RU,
            title_en=SearchTest.TITLE_EN,
            body_en=SearchTest.BODY_EN,
            author=author,
            category=category,
            publish=timezone.now().replace(day=1),
        )
        PostFactory.create_batch(3, author=author, category=category, publish=timezone.now().replace(day=2))
        cls.queryset = Post.objects.all()

    def test_search_by_tag(self):
        # Создаём тег по которому будем делать поиск и присваиваем его посту
        expected_tag = Tag.objects.create(name='Desired tag', slug='desired-tag')
        self.expected_post.tags.add(expected_tag)

        # Вызываем тестируемую функцию для получения объекта тега и отфильтрованного по тегу queryset-а
        fact_tag, fact_filtered_queryset = search_by_tag(expected_tag.slug, self.queryset)  # передаём slug тега

        # Проверка №1. Отфильтрованный queryset содержит только пост с ожидаемым тегом
        self.assertQuerySetEqual(
            fact_filtered_queryset,
            [
                self.expected_post,
            ],
        )

        # Проверка №2. Объект тега является тем, который мы ожидаем
        self.assertEqual(fact_tag, expected_tag)

    def test_search_by_date(self):
        # Дата текущего месяца по которой будут фильтроваться посты
        desired_day = 1

        # Получаем все посты за указанный день текущего месяца и проверяем на соответствие
        fact_filtered_queryset = search_by_date(desired_day, self.queryset)
        self.assertQuerySetEqual(
            fact_filtered_queryset,
            [
                self.expected_post,
            ],
        )

    @parameterized.expand(
        [
            ('title_ru', TITLE_RU, LANGUAGES[0][0]),  # поиск по русскому заголовку
            ('body_ru', BODY_RU, LANGUAGES[0][0]),  # поиск по русскому содержанию
            ('title_en', TITLE_EN, LANGUAGES[1][0]),  # поиск по английскому заголовку
            ('body_en', BODY_EN, LANGUAGES[1][0]),  # поиск по английскому содержанию
        ]
    )
    def test_search_by_q(self, _, search_text, language):
        fact_searched_queryset = search_by_q(search_text, self.queryset, language)
        self.assertQuerySetEqual(
            fact_searched_queryset,
            [
                self.expected_post,
            ],
        )
