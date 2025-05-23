from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from blog_by_me.settings import KEY_AUTHORS_LIST
from tests.users.factories import CustomUserFactory
from users.models import CustomUser


class AuthorsViewTest(TestCase):
    """Тестирование представления AuthorsView(ListView)"""

    @classmethod
    def setUpTestData(cls):
        activate('ru')
        CustomUserFactory.create_batch(5)
        cls.expected_queryset = CustomUser.objects.all()

    def get_response(self):
        return self.client.get(reverse('author_list'))

    def test_view_url(self):
        response = self.client.get('/ru/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_name(self):
        response = self.get_response()
        self.assertEqual(response.status_code, 200)

    def test_view_template_name(self):
        response = self.get_response()
        self.assertTemplateUsed(response, 'users/author_list.html')

    def test_view_context_object_name(self):
        response = self.get_response()
        self.assertTrue('authors' in response.context)

    @mock.patch('users.views.get_cached_objects_or_queryset')
    def test_view_get_queryset_return_mock(self, mock_get_objects_list):
        _ = self.get_response()
        mock_get_objects_list.assert_called_once_with(KEY_AUTHORS_LIST)

    def test_view_get_queryset_return_not_mock(self):
        response = self.get_response()
        fact_queryset = response.context['authors']
        self.assertQuerySetEqual(fact_queryset, self.expected_queryset)
