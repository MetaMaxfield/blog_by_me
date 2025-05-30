from captcha.widgets import ReCaptchaV3
from django import forms
from django.forms import RadioSelect
from django.test import TestCase

from blog.forms import CommentsForm, RatingForm
from blog.models import Comment, Rating
from blog_by_me.settings import RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY
from tests.blog.factories import MarkFactory


class CommentsFormTest(TestCase):
    """Тестирование формы CommentsForm"""

    @classmethod
    def setUpTestData(cls):
        cls.form = CommentsForm()

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
        self.assertEqual(fact_model, Comment)

    def test_form_fields(self):
        fact_fields = self.form._meta.fields
        self.assertEqual(fact_fields, ('name', 'email', 'text', 'captcha'))

    def test_form_widgets(self):
        fact_widgets = self.form._meta.widgets
        expected_widgets = {
            'name': forms.TextInput(attrs={'class': 'span10', 'data-required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'span10', 'data-required': 'true', 'data-type': 'email'}),
            'text': forms.Textarea(attrs={'class': 'span10', 'data-trigger': 'keyup', 'id': 'contactcomment'}),
        }
        for field, expected_widget in expected_widgets.items():
            # Тест №1. Проверка виджета поля
            fact_widget = type(fact_widgets[field])
            self.assertEqual(fact_widget, type(expected_widget))

            # Тест №2. Проверка атрибутов у виджетов
            fact_widget_attrs = fact_widgets[field].attrs
            expected_widget_attrs = expected_widget.attrs
            self.assertEqual(fact_widget_attrs, expected_widget_attrs)


class RatingFormTest(TestCase):
    """Тестирование формы RatingForm"""

    @classmethod
    def setUpTestData(cls):
        cls.form = RatingForm()

    def test_rating_captcha_widget(self):
        fact_widget = type(self.form.fields['rating_captcha'].widget)
        self.assertEqual(fact_widget, ReCaptchaV3)

    def test_rating_captcha_public_key(self):
        fact_public_key = self.form.fields['rating_captcha'].public_key
        self.assertEqual(fact_public_key, RECAPTCHA_PUBLIC_KEY)

    def test_rating_captcha_private_key(self):
        fact_private_key = self.form.fields['rating_captcha'].private_key
        self.assertEqual(fact_private_key, RECAPTCHA_PRIVATE_KEY)

    def test_rating_captcha_label(self):
        fact_label = self.form.fields['rating_captcha'].label
        self.assertEqual(fact_label, 'ReCAPTCHA')

    def test_mark_queryset(self):
        fact_queryset = self.form.fields['mark'].queryset
        mark1 = MarkFactory.create()
        mark2 = MarkFactory.create(nomination='Дизлайк', value=-1)
        self.assertQuerySetEqual(fact_queryset, [mark1, mark2])

    def test_mark_widget(self):
        fact_widget = type(self.form.fields['mark'].widget)
        self.assertEqual(fact_widget, RadioSelect)

    def test_mark_empty_label(self):
        fact_empty_label = self.form.fields['mark'].empty_label
        self.assertIsNone(fact_empty_label)

    def test_form_model(self):
        fact_model = self.form._meta.model
        self.assertEqual(fact_model, Rating)

    def test_form_fields(self):
        fact_fields = self.form._meta.fields
        self.assertEqual(fact_fields, ('mark', 'rating_captcha'))
