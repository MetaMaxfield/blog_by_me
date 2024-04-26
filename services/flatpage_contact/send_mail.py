import os
from django.core.mail import send_mail
from dotenv import load_dotenv


load_dotenv()


def send(user_mail: str) -> None:
    """Отправка электронного письма при получении обратной связи через форму"""
    send_mail(
        'Запрос к администрации веб-приложения MAXFIELD.',
        'Ваш запрос зарегистрирован. Ожидайте обратную связь на данный адрес эл. почты. ',
        os.getenv('MAIL_KEY'),
        [user_mail],
        fail_silently=False
    )
