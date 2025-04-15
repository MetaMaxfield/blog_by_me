from django.test import RequestFactory, TestCase

from services.client_ip import get_client_ip


class GetClientIpTest(TestCase):
    """Тестирование функции get_client_ip"""

    @classmethod
    def setUp(cls):
        cls.request = RequestFactory().get('/')

    def test_get_ip_with_proxy(self):
        self.request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.195, 198.51.100.42, 127.0.0.1'
        fact_ip = get_client_ip(self.request)
        self.assertEqual(fact_ip, '203.0.113.195')

    def test_get_ip_without_proxy(self):
        fact_ip = get_client_ip(self.request)
        self.assertEqual(fact_ip, '127.0.0.1')
