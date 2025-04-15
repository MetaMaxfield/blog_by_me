from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from blog_by_me.settings import STATIC_URL
from services.users.validator import username_validator
from tests.blog.factories import CategoryFactory, PostFactory
from tests.users.factories import CustomUserFactory, GroupFactory
from users.models import CustomUser


class CustomUserModelTest(TestCase):
    """Тестирование модели CustomUser"""

    @classmethod
    def setUpTestData(cls):
        CustomUserFactory.create()

    @classmethod
    def setUp(cls):
        cls.custom_user = CustomUser.objects.first()

    def test_username_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('username').verbose_name
        self.assertEqual(fact_verbose_name, 'username')

    def test_username_max_length(self):
        fact_max_length = self.custom_user._meta.get_field('username').max_length
        self.assertEqual(fact_max_length, 150)

    def test_username_unique(self):
        fact_unique = self.custom_user._meta.get_field('username').unique
        self.assertTrue(fact_unique)

    def test_username_help_text(self):
        fact_help_text = self.custom_user._meta.get_field('username').help_text
        self.assertEqual(
            fact_help_text, 'Обязательное условие. 150 символов или меньше. Только буквы, цифры, пробелы и @/./+/-/_.'
        )

    def test_username_validators(self):
        fact_validators = self.custom_user._meta.get_field('username').validators
        self.assertIn(username_validator, fact_validators)

    def test_username_error_messages(self):
        fact_error_messages = self.custom_user._meta.get_field('username').error_messages['unique']
        self.assertEqual(fact_error_messages, 'Пользователь с таким именем уже существует.')

    def test_birthday_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('birthday').verbose_name
        self.assertEqual(fact_verbose_name, 'Дата рождения')

    def test_birthday_null(self):
        fact_null = self.custom_user._meta.get_field('birthday').null
        self.assertTrue(fact_null)

    def test_birthday_blank(self):
        fact_blank = self.custom_user._meta.get_field('birthday').blank
        self.assertTrue(fact_blank)

    def test_description_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('description').verbose_name
        self.assertEqual(fact_verbose_name, 'Информация об пользователе')

    def test_description_blank(self):
        fact_blank = self.custom_user._meta.get_field('description').blank
        self.assertTrue(fact_blank)

    def test_image_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('image').verbose_name
        self.assertEqual(fact_verbose_name, 'Изображение пользователя')

    def test_image_upload_to(self):
        fact_upload_to = self.custom_user._meta.get_field('image').upload_to
        self.assertEqual(fact_upload_to, 'users/')

    def test_image_null(self):
        fact_null = self.custom_user._meta.get_field('image').null
        self.assertTrue(fact_null)

    def test_image_blank(self):
        fact_blank = self.custom_user._meta.get_field('image').blank
        self.assertTrue(fact_blank)

    def test_total_likes_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('total_likes').verbose_name
        self.assertEqual(fact_verbose_name, 'Общее количество лайков')

    def test_total_likes_default(self):
        fact_default = self.custom_user._meta.get_field('total_likes').default
        self.assertEqual(fact_default, 0)

    def test_is_staff_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('is_staff').verbose_name
        self.assertEqual(fact_verbose_name, 'Статус персонала')

    def test_is_staff_default(self):
        fact_default = self.custom_user._meta.get_field('is_staff').default
        self.assertTrue(fact_default)

    def test_is_staff_help_text(self):
        fact_help_text = self.custom_user._meta.get_field('is_staff').help_text
        self.assertEqual(fact_help_text, 'Определяет, может ли пользователь войти ' 'на сайт администрирования.')

    def test_email_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.get_field('email').verbose_name
        self.assertEqual(fact_verbose_name, 'E-mail')

    def test_email_blank(self):
        fact_blank = self.custom_user._meta.get_field('email').blank
        self.assertFalse(fact_blank)

    def test_get_image_url(self):
        # проверка метода для неустановленного изображения (изображения по умолчанию)
        expected_url_with_blank_image = STATIC_URL + 'img/comment_icon.png'
        fact_image_url = self.custom_user.get_image_url()
        self.assertEqual(fact_image_url, expected_url_with_blank_image)

        # проверка метода для установленного изображения
        self.custom_user.image = SimpleUploadedFile('avatar.jpeg', b'fake image content', content_type='image/jpeg')
        self.custom_user.save()
        fact_image_url = self.custom_user.get_image_url()
        self.assertEqual(fact_image_url, self.custom_user.image.url)

    def test_get_user_groups(self):
        group = GroupFactory.create()
        self.custom_user.groups.add(group)

        # проверка метода при отсутствии прав администратора
        fact_groups = self.custom_user.get_user_groups()
        self.assertEqual(
            fact_groups,
            [
                group.name,
            ],
        )

        # проверка метода при наличии прав администратора
        self.custom_user.is_superuser = True
        self.custom_user.save()
        fact_groups = self.custom_user.get_user_groups()
        self.assertEqual(fact_groups, ['Администратор', group.name])

    def test_get_user_groups_short_description(self):
        fact_short_description = self.custom_user.__class__.get_user_groups.short_description
        self.assertEqual(fact_short_description, 'Группы пользователя')

    def test_get_last_posts_user(self):
        # mock для сигнала "post_save"
        with mock.patch('django.db.models.signals.post_save.send'):

            # Проверка №1. Недоступность постов при отложенной публикации или "draft=True"
            category = CategoryFactory.create()
            PostFactory.create(author=self.custom_user, category=category, draft=True)
            PostFactory.create(
                author=self.custom_user, category=category, publish=timezone.now() + timezone.timedelta(3)
            )
            fact_last_posts = self.custom_user.get_last_posts_user()
            self.assertQuerySetEqual(fact_last_posts, [])

            # создание постов для последующих проверок
            PostFactory.create(author=self.custom_user, category=category)
            post2 = PostFactory.create(author=self.custom_user, category=category)
            post3 = PostFactory.create(author=self.custom_user, category=category)
            post4 = PostFactory.create(author=self.custom_user, category=category)
            fact_last_posts = self.custom_user.get_last_posts_user()

            # Проверка №2. Для запроса к БД используется 'select_related()'
            with self.assertNumQueries(1):
                for post in fact_last_posts:
                    _ = post.category
                    _ = post.author

            # Проверка №3. Количество постов (выводятся последние три поста)
            self.assertQuerySetEqual(fact_last_posts, [post4, post3, post2])

    def test_object_name_is_username(self):
        expected_object_name = self.custom_user.username
        self.assertEqual(str(self.custom_user), expected_object_name)

    def test_model_verbose_name(self):
        fact_verbose_name = self.custom_user._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Пользователь')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.custom_user._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Пользователи')
