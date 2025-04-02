from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ValidationError
from django.db.models import CASCADE
from django.test import TestCase

from flatpage_contact.models import NewFlatpage
from tests.flatpage_contact.factories import NewFlatpageFactory


class NewFlatpageModelTest(TestCase):
    """Тестирование модели NewFlatpage"""

    @classmethod
    def setUpTestData(cls):
        NewFlatpageFactory.create()

    @classmethod
    def setUp(cls):
        cls.new_flatpage = NewFlatpage.objects.first()

    def test_flatpage_to_model(self):
        fact_to_model = self.new_flatpage._meta.get_field('flatpage').remote_field.model
        self.assertEqual(fact_to_model, FlatPage)

    def test_flatpage_on_delete(self):
        fact_on_delete = self.new_flatpage._meta.get_field('flatpage').remote_field.on_delete
        self.assertEqual(fact_on_delete, CASCADE)

    def test_google_maps_html_verbose_name(self):
        fact_verbose_name = self.new_flatpage._meta.get_field('google_maps_html').verbose_name
        self.assertEqual(fact_verbose_name, 'HTML-код Google Maps')

    def test_google_maps_html_default(self):
        fact_default = self.new_flatpage._meta.get_field('google_maps_html').default
        self.assertEqual(fact_default, '')

    def test_description_verbose_name(self):
        fact_verbose_name = self.new_flatpage._meta.get_field('description').verbose_name
        self.assertEqual(fact_verbose_name, 'Основной текстовый контент страницы')

    def test_description_default(self):
        fact_default = self.new_flatpage._meta.get_field('description').default
        self.assertEqual(fact_default, '')

    def test_email_contact_verbose_name(self):
        fact_verbose_name = self.new_flatpage._meta.get_field('email_contact').verbose_name
        self.assertEqual(fact_verbose_name, 'Эл. почта для контакта')

    def test_email_contact_default(self):
        fact_default = self.new_flatpage._meta.get_field('email_contact').default
        self.assertEqual(fact_default, '')

    def test_phone1_num_verbose_name(self):
        fact_verbose_name = self.new_flatpage._meta.get_field('phone1_num').verbose_name
        self.assertEqual(fact_verbose_name, 'Мобильный телефон')

    def test_phone2_num_verbose_name(self):
        fact_verbose_name = self.new_flatpage._meta.get_field('phone2_num').verbose_name
        self.assertEqual(fact_verbose_name, 'Стационарный телефон')

    def test_object_name_is_flatpage_title(self):
        expected_object_name = 'О нас'
        self.assertEqual(str(self.new_flatpage), expected_object_name)

    def test_save(self):
        with self.assertRaises(ValidationError):
            NewFlatpageFactory.create()

    def test_model_verbose_name(self):
        fact_verbose_name = self.new_flatpage._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Содержание страницы')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.new_flatpage._meta.verbose_name
        self.assertEqual(fact_verbose_name_plural, 'Содержание страницы')
