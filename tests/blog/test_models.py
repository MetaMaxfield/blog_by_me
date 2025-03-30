from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from django.test import TestCase

from blog.models import Category, Video


class CategoryModelTest(TestCase):
    """Тестирование модели Category"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Наука', description='Категория о науке', url='science')

    @classmethod
    def setUp(cls):
        cls.category = Category.objects.get(name='Наука')

    def test_name_verbose_name(self):
        fact_verbose_name = self.category._meta.get_field('name').verbose_name
        self.assertEqual(fact_verbose_name, 'Категория')

    def test_name_max_length(self):
        fact_max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(fact_max_length, 150)

    def test_description_verbose_name(self):
        fact_verbose_name = self.category._meta.get_field('description').verbose_name
        self.assertEqual(fact_verbose_name, 'Описание')

    def test_url_max_length(self):
        fact_max_length = self.category._meta.get_field('url').max_length
        self.assertEqual(fact_max_length, 160)

    def test_url_unique(self):
        fact_unique = self.category._meta.get_field('url').unique
        self.assertTrue(fact_unique)

    def test_object_name_is_name(self):
        expected_object_name = self.category.name
        self.assertEqual(str(self.category), expected_object_name)

    def test_model_verbose_name(self):
        fact_verbose_name = self.category._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Категория')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.category._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Категории')


class VideoModelTest(TestCase):
    """Тестирование модели Video"""

    @classmethod
    def setUpTestData(cls):
        Video.objects.create(
            title='Котята',
            description='Забавные котята',
            file=SimpleUploadedFile("cats.mp4", b"fake video content", content_type="video/mp4"),
        )

    @classmethod
    def setUp(cls):
        cls.video = Video.objects.get(title='Котята')

    def test_title_max_lenght(self):
        fact_max_length = self.video._meta.get_field('title').max_length
        self.assertEqual(fact_max_length, 100)

    def test_title_verbose_name(self):
        fact_verbose_name = self.video._meta.get_field('title').verbose_name
        self.assertEqual(fact_verbose_name, 'Заголовок видео')

    def test_description_verbose_name(self):
        fact_verbose_name = self.video._meta.get_field('description').verbose_name
        self.assertEqual(fact_verbose_name, 'Описание видео')

    def test_file_upload_to(self):
        fact_upload_to = self.video._meta.get_field('file').upload_to
        self.assertEqual(fact_upload_to, 'video/')

    def test_file_validators(self):
        fact_validators = self.video._meta.get_field('file').validators
        self.assertEqual(fact_validators, [FileExtensionValidator(allowed_extensions=['mp4'])])

    def test_file_verbose_name(self):
        fact_verbose_name = self.video._meta.get_field('file').verbose_name
        self.assertEqual(fact_verbose_name, 'Видеофайл')

    def test_create_at_auto_now_add(self):
        fact_auto_now_add = self.video._meta.get_field('create_at').auto_now_add
        self.assertTrue(fact_auto_now_add)

    def test_object_name_is_title(self):
        expected_object_name = self.video.title
        self.assertEqual(str(self.video), expected_object_name)

    def test_model_ordering(self):
        fact_ordering = self.video._meta.ordering
        self.assertEqual(fact_ordering, ('-create_at',))

    def test_model_verbose_name(self):
        fact_verbose_name = self.video._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Видеозапись')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.video._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Видеозаписи')
