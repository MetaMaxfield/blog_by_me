import datetime
from re import search, split

from django.db.models import QuerySet
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber


def service_ru_plural(value: int, variants: str) -> str:
    """Логика изменения окончания слова в зависимости от количества"""
    variants = variants.split(',')
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants[variant]


def service_share_url_format(url: str) -> str:
    """Логика работы форматирования URL адреса для блока "Поделиться"""
    if search(r'/[\w?%=/]+$', url):
        url, _ = split(r'/[\w?%=/]+$', url)
    return url


def add_posts_days_in_list(qs_calendar: QuerySet) -> set[int]:
    """Добавление в список дней, в которые публиковались посты"""
    posts_days = []
    for day in qs_calendar:
        posts_days.extend(day)
    return set(posts_days)


def service_age_tag(birthday: datetime.date) -> int:
    """Логика расчёта возраста пользователя"""
    today = timezone.now().date()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def service_format_phone_num(num: PhoneNumber) -> str:
    """Логика форматирования номера телефона для шаблона"""
    num = str(num)
    return f'{num[0:2]} ({num[2:5]}) {num[5:8]}-{num[8:10]}-{num[10:12]}'
