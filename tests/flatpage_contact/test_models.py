from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ValidationError
from django.db.models import CASCADE
from django.test import TestCase

from flatpage_contact.models import Contact, NewFlatpage
from tests.flatpage_contact.factories import ContactFactory, NewFlatpageFactory


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


class ContactModelTest(TestCase):
    """Тестирование модели Contact"""

    @classmethod
    def setUpTestData(cls):
        ContactFactory.create()

    @classmethod
    def setUp(cls):
        cls.contact = Contact.objects.first()

    def test_name_verbose_name(self):
        fact_verbose_name = self.contact._meta.get_field('name').verbose_name
        self.assertEqual(fact_verbose_name, 'Имя')

    def test_email_verbose_name(self):
        fact_verbose_name = self.contact._meta.get_field('email').verbose_name
        self.assertEqual(fact_verbose_name, 'Эл. почта')

    def test_phone_verbose_name(self):
        fact_verbose_name = self.contact._meta.get_field('phone').verbose_name
        self.assertEqual(fact_verbose_name, 'Телефон')

    def test_message_verbose_name(self):
        fact_verbose_name = self.contact._meta.get_field('message').verbose_name
        self.assertEqual(fact_verbose_name, 'Сообщение')

    def test_date_auto_now_add(self):
        fact_auto_now_add = self.contact._meta.get_field('date').auto_now_add
        self.assertTrue(fact_auto_now_add)

    def test_feedback_verbose_name(self):
        fact_verbose_name = self.contact._meta.get_field('feedback').verbose_name
        self.assertEqual(fact_verbose_name, 'Обрантая связь')

    def test_feedback_default(self):
        fact_default = self.contact._meta.get_field('feedback').default
        self.assertFalse(fact_default)

    def test_object_name_is_email(self):
        expected_object_name = self.contact.email
        self.assertEqual(str(self.contact), expected_object_name)

    def test_model_verbose_name(self):
        fact_verbose_name = self.contact._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Запрос от пользователя блога')

    def test_verbose_name_plural(self):
        fact_verbose_name_plural = self.contact._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Запросы от пользователей блога')
