from django.test import TestCase

from blog.models import Category


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
