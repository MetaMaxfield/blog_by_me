from captcha.widgets import ReCaptchaV3
from django import forms
from django.test import TestCase
from phonenumber_field.widgets import RegionalPhoneNumberWidget

from blog_by_me.settings import RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY
from flatpage_contact.forms import ContactForm
from flatpage_contact.models import Contact


class ContactFormTest(TestCase):
    """Тестирование формы ContactForm"""

    @classmethod
    def setUpTestData(cls):
        cls.form = ContactForm()

    def test_captcha_widget(self):
        fact_widget = type(self.form.fields['captcha'].widget)
        self.assertEqual(fact_widget, ReCaptchaV3)

    def test_captcha_public_key(self):
        fact_public_key = self.form.fields['captcha'].public_key
        self.assertEqual(fact_public_key, RECAPTCHA_PUBLIC_KEY)

    def test_captcha_private_key(self):
        fact_private_key = self.form.fields['captcha'].private_key
        self.assertEqual(fact_private_key, RECAPTCHA_PRIVATE_KEY)

    def test_captcha_label(self):
        fact_label = self.form.fields['captcha'].label
        self.assertEqual(fact_label, 'ReCAPTCHA')

    def test_form_model(self):
        fact_model = self.form._meta.model
        self.assertEqual(fact_model, Contact)

    def test_form_fields(self):
        fact_fields = self.form._meta.fields
        self.assertEqual(fact_fields, ('name', 'email', 'phone', 'message', 'captcha'))

    def test_form_widgets(self):
        fact_widgets = self.form._meta.widgets
        expected_widgets = {
            'name': forms.TextInput(attrs={'class': 'span10', 'data-required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'span10', 'data-required': 'true', 'data-type': 'email'}),
            'phone': RegionalPhoneNumberWidget(
                attrs={'class': 'span10', 'data-trigger': 'keyup', 'data-type': 'phone'}
            ),
            'message': forms.Textarea(attrs={'class': 'span10', 'data-trigger': 'keyup'}),
        }
        for field, expected_widget in expected_widgets.items():
            # Тест №1. Проверка виджета поля
            fact_widget = type(fact_widgets[field])
            self.assertEqual(fact_widget, type(expected_widget))

            # Тест №2. Проверка атрибутов у виджетов
            fact_widget_attrs = fact_widgets[field].attrs
            expected_widget_attrs = expected_widget.attrs
            self.assertEqual(fact_widget_attrs, expected_widget_attrs)
