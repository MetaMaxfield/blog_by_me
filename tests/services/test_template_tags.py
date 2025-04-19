from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from parameterized import parameterized

from blog.models import Post
from services.template_tags import add_posts_days_in_list, service_age_tag, service_ru_plural, service_share_url_format
from tests.blog.factories import CategoryFactory, PostFactory
from tests.users.factories import CustomUserFactory


class RuPluralTest(SimpleTestCase):
    """Тестирование функции service_ru_plural"""

    @parameterized.expand(
        [
            ('1_value', 1, 'файл,файла,файлов', 'файл'),  # оканчивается на 1, не на 11
            ('2_value', 2, 'файл,файла,файлов', 'файла'),  # оканчивается на 2, не на 12
            ('4_value', 4, 'файл,файла,файлов', 'файла'),  # оканчивается на 4, не на 14
            ('5_value', 5, 'файл,файла,файлов', 'файлов'),  # оканчивается на 5 — всегда множественное
            ('11_value', 11, 'файл,файла,файлов', 'файлов'),  # 11 — исключение, всегда множественное
            ('14_value', 14, 'файл,файла,файлов', 'файлов'),  # 14 — исключение, всегда множественное
            ('21_value', 21, 'файл,файла,файлов', 'файл'),  # оканчивается на 1, не на 11
            ('22_value', 22, 'файл,файла,файлов', 'файла'),  # оканчивается на 2, не на 12
            ('25_value', 25, 'файл,файла,файлов', 'файлов'),  # оканчивается на 5 — всегда множественное
            ('101_value', 101, 'файл,файла,файлов', 'файл'),  # оканчивается на 1, не на 11
            ('111_value', 111, 'файл,файла,файлов', 'файлов'),  # оканчивается на 11 — исключение
            ('1001_value', 1001, 'файл,файла,файлов', 'файл'),  # оканчивается на 1, не на 11
            ('1014_value', 1014, 'файл,файла,файлов', 'файлов'),  # оканчивается на 14 — исключение
        ]
    )
    def test_service_ru_plural(self, _, value, variants, expected_variant):
        fact_variant = service_ru_plural(value, variants)
        self.assertEqual(fact_variant, expected_variant)


class ShareUrlFormatTest(SimpleTestCase):
    """Тестирование функции service_share_url_format"""

    def test_service_share_url_format(self):
        fact_url = service_share_url_format('http://127.0.0.1:8000/ru/')
        self.assertEqual(fact_url, 'http://127.0.0.1:8000')


class AddPostsDaysInListTest(TestCase):
    """Тестирование функции add_posts_days_in_list"""

    def test_add_posts_days_in_list(self):
        # создаём автора и категорию для постов
        category = CategoryFactory.create()
        author = CustomUserFactory.create()

        # создаём два поста с датой "1" и один пост с датой "2"
        PostFactory.create_batch(2, category=category, author=author, publish=timezone.now().replace(day=1))
        PostFactory.create(category=category, author=author, publish=timezone.now().replace(day=2))

        # получаем QuerySet с датами постов
        queryset = Post.objects.all().values_list('publish__day')

        # получаем на основе переданного QuerySet числа дней публикации
        fact_days = add_posts_days_in_list(queryset)

        # проверям что вовзращены только уникальные числа дней публикации
        self.assertEqual(fact_days, {1, 2})


class ServiceAgeTag(SimpleTestCase):
    """Тестирование функции service_age_tag"""

    @parameterized.expand(
        [
            ('1', timezone.timedelta(days=-2), 1),  # День рождения был более года назад, возраст должен быть 1
            ('0', timezone.timedelta(days=2), 0),  # День рождения ещё не наступил, возраст должен быть 0
        ]
    )
    def test_service_age_tag(self, _, timedelta, expected_years_old):
        birthday = timezone.now().date() - timezone.timedelta(days=365) + timedelta
        fact_years_old = service_age_tag(birthday)
        self.assertEqual(fact_years_old, expected_years_old)
