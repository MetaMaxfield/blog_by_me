from unittest import mock

from django.db.models import Prefetch
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from parameterized import parameterized

from blog.models import Category, Post
from blog_by_me import settings
from services import queryset
from services.queryset import _qs_categories_list, _qs_post_list, qs_definition
from tests.blog.factories import CategoryFactory, PostFactory
from tests.users.factories import CustomUserFactory


class NotDefiniteQSTest(SimpleTestCase):
    """Тестирование функции not_definite_qs"""

    def test_not_definite_qs(self):
        # Проверка №1. Проверка на вызов ошибки
        with self.assertRaises(Exception) as error:
            queryset.not_definite_qs()

        # Проверка №2. Проверка текста с содержанием ошибки
        expected_message_error = 'Ключ для получения queryset не найден.'
        self.assertEqual(str(error.exception), expected_message_error)


class QSDefinitionTest(SimpleTestCase):
    """Тестирование функции qs_definition"""

    @parameterized.expand(
        [
            ('for_posts_list', '_qs_post_list', settings.KEY_POSTS_LIST),
            ('for_qs_post_detail', '_qs_post_detail', settings.KEY_POST_DETAIL),
            ('for_categories_list', '_qs_categories_list', settings.KEY_CATEGORIES_LIST),
            ('for_videos_list', '_qs_videos_list', settings.KEY_VIDEOS_LIST),
            ('for_contact_flatpage', '_qs_contact_flatpage', settings.KEY_CONTACT_FLATPAGE),
            ('for_author_list', '_qs_author_list', settings.KEY_AUTHORS_LIST),
            ('for_author_detail', '_qs_author_detail', settings.KEY_AUTHOR_DETAIL),
            ('for_top_posts', '_qs_top_posts', settings.KEY_TOP_POSTS),
            ('for_last_posts', '_qs_last_posts', settings.KEY_LAST_POSTS),
            ('for_all_tags', '_qs_all_tags', settings.KEY_ALL_TAGS),
            ('for_days_posts_in_current_month', '_qs_days_posts_in_current_month', settings.KEY_POSTS_CALENDAR),
            # вызов функции not_definite_qs при неизвестном ключе
            ('for_not_definite_qs', 'not_definite_qs', 'UNSPECIFIED_KEY'),
        ]
    )
    def test_qs_definition(self, _, name_func, qs_key):
        """Для каждого кейса передаётся ключ qs_key и имя функции name_func, которую нужно замокать"""

        # фиктивные данные для имитации поведения замоканной функции
        expected_return = 'mock'
        fake_slug_or_pk = 'fake_slug_or_pk'

        # мокаем соответствующую функцию и вызываем тестируемую qs_definition
        with mock.patch(f'services.queryset.{name_func}', return_value=expected_return) as mocked_func:
            fact_return = qs_definition(qs_key, fake_slug_or_pk)

            # Проверка №1. Функция вызывается с переданным slug_or_pk
            mocked_func.assert_called_once_with(fake_slug_or_pk)

        # Проверка №2. Возвращаемое значение совпадает с ожидаемым
        self.assertEqual(fact_return, expected_return)


class QSPostListTest(TestCase):
    """Тестирование функции _qs_post_list"""

    @classmethod
    def setUpTestData(cls):
        # фиксируем настоящее время для использования в качестве мока
        # для тестируемой функции и для создания тестовых постов
        # (необходимо для правильного тестирования в test__qs_post_list_main_query())
        cls.now_time = timezone.now()

        author = CustomUserFactory.create()
        category = CategoryFactory.create()

        # создание дополнительных двух постов, которые не должны пройти фильтрацию
        PostFactory.create(author=author, category=category, publish=cls.now_time + timezone.timedelta(seconds=10))
        with mock.patch('django.db.models.signals.post_save.send'):  # заглушка для срабатывания сигнала при draft=True
            PostFactory.create(author=author, category=category, draft=True)

        # создание четырёх опубликованных постов
        PostFactory.create_batch(4, author=author, category=category, publish=cls.now_time)

        # получение данных из тестируемой функции с зафиксированным временем self.now_time
        with mock.patch('services.queryset.timezone.now', return_value=cls.now_time):
            cls.fact_posts = _qs_post_list()

    def test__qs_post_list_num_queries(self):
        """
        Тестирование количества запросов.
        Допустимое количество запросов с описанием:
        1. Основной запрос с использованием select_related
        2. Дополнительный через prefetch_related('tagged_items__tag')
        3. Дополнительный через prefetch_related(Prefetch('author', CustomUser.objects.only('username', 'id'))
        """
        with self.assertNumQueries(3):
            list(self.fact_posts)

    def test__qs_post_list_filter(self):
        """Тестирование фильтрации"""
        expected_posts = Post.objects.filter(draft=False, publish__lte=timezone.now())
        self.assertQuerysetEqual(expected_posts, self.fact_posts)

    def test__qs_post_list_main_query(self):
        """
        Проверяет что запрос к БД через ORM реализован в следующем виде:

        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .select_related(
            'category',
        )
        .prefetch_related('tagged_items__tag', Prefetch('author', CustomUser.objects.only('username', 'id')))
        .defer('video', 'created', 'updated', 'draft')
        .annotate(ncomments=Count('comments'))

        ВАЖНО: Проверка .prefetch_related осуществляется отдельно в test__qs_post_list_prefetch_query()
        """
        fact_query = str(self.fact_posts.query)
        expected_query = (
            'SELECT "blog_post"."id", "blog_post"."title", "blog_post"."title_ru", "blog_post"."title_en", '
            '"blog_post"."url", "blog_post"."author_id", "blog_post"."category_id", "blog_post"."body", '
            '"blog_post"."body_ru", "blog_post"."body_en", "blog_post"."image", "blog_post"."publish", '
            'COUNT("blog_comment"."id") AS "ncomments", "blog_category"."id", "blog_category"."name", '
            '"blog_category"."name_ru", "blog_category"."name_en", "blog_category"."description", '
            '"blog_category"."description_ru", "blog_category"."description_en", "blog_category"."url" FROM '
            '"blog_post" LEFT OUTER JOIN "blog_comment" ON ("blog_post"."id" = "blog_comment"."post_id") LEFT OUTER '
            'JOIN "blog_category" ON ("blog_post"."category_id" = "blog_category"."id") WHERE (NOT "blog_post"."draft" '
            f'AND "blog_post"."publish" <= {self.now_time}) GROUP BY "blog_post"."id", '
            '"blog_category"."id" ORDER BY "blog_post"."publish" DESC, "blog_post"."id" DESC'
        )
        self.assertEqual(expected_query, fact_query)

    def test__qs_post_list_prefetch_query(self):
        """Тестирование дополнительных запросов из prefetch_related."""
        prefetch_related_lookups = list(self.fact_posts._prefetch_related_lookups)

        # Проверка №1. Наличие префетча 'tagged_items__tag' (строкой)
        self.assertIn('tagged_items__tag', prefetch_related_lookups)

        # Тестируем наличие .prefetch_related(Prefetch('author', CustomUser.objects.only('username', 'id'))
        for p in prefetch_related_lookups:  # ищем необходимый дополнительный запрос
            if isinstance(p, Prefetch) and p.prefetch_to == 'author':
                fact_prefetch2_query = str(p.queryset.query)
                break
        expected_prefetch_query = (
            'SELECT "users_customuser"."id", "users_customuser"."username" FROM "users_customuser"'
        )
        # Проверка №2. Наличие префетча 'author' с кастомным queryset через Prefetch (по SQL-запросу)
        self.assertEqual(fact_prefetch2_query, expected_prefetch_query)


class QSCategoriesListTest(TestCase):
    """Тестирование функции _qs_categories_list"""

    def test__qs_categories_list(self):
        CategoryFactory.create_batch(5)

        # получение ожидаемого списка категорий и категорий из тестируемой функции
        # с дополнительной сортировкой, так как она явно не задана
        expected_categories = Category.objects.all().order_by('id')
        fact_categories = _qs_categories_list().order_by('id')

        self.assertQuerysetEqual(fact_categories, expected_categories)
