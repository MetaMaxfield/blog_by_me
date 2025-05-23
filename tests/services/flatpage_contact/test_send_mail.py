from unittest import mock

from django.test import SimpleTestCase

from blog_by_me.settings import EMAIL_HOST_USER
from services.flatpage_contact.send_mail import send


class SendMailTest(SimpleTestCase):
    """Тестировании функции send"""

    @mock.patch('services.flatpage_contact.send_mail.send_mail')
    def test_send_mail(self, mock_send_mail):
        email = 'testmail@test.com'
        send(email)
        mock_send_mail.assert_called_once_with(
            'Запрос к администрации веб-приложения MAXFIELD.',
            'Ваш запрос зарегистрирован. Ожидайте обратную связь на данный адрес эл. почты. ',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
