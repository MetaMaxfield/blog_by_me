from unittest import mock

from django.test import SimpleTestCase, TestCase
from parameterized import parameterized

from blog.models import Category
from blog_by_me import settings
from services import queryset
from services.queryset import _qs_categories_list, qs_definition
from tests.blog.factories import CategoryFactory


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


class QSCategoriesListTest(TestCase):
    """Тестирование функции _qs_categories_list"""

    def test__qs_categories_list(self):
        CategoryFactory.create_batch(5)

        # получение ожидаемого списка категорий и категорий из тестируемой функции
        # с дополнительной сортировкой, так как она явно не задана
        expected_categories = Category.objects.all().order_by('id')
        fact_categories = _qs_categories_list().order_by('id')

        self.assertQuerysetEqual(fact_categories, expected_categories)
