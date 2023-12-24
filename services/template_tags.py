from re import split, search
from blog_by_me.settings import CURRENT_DATETIME


def service_ru_plural(value, variants):
    """Логика изменения окончания слова в зависимости от количества"""
    variants = variants.split(',')
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants[variant]


def service_share_url_format(url):
    """Логика работы форматирования URL адреса для блока "Поделиться"""
    if search(r'/[\w?%=/]+$', url):
        result, _ = split(r'/[\w?%=/]+$', url)
        return result
    else:
        return url


def add_posts_days_in_list(qs_calendar):
    """Добавление в список дней, в которые публиковались посты"""
    posts_days = []
    [posts_days.append(*x) for x in qs_calendar]
    return posts_days


def service_age_tag(birthday):
    """Логика расчёта возраста пользователя"""
    today = CURRENT_DATETIME.date()
    result = (today.year - birthday.year)
    if birthday.month >= today.month and birthday.day > today.day:
        result -= 1
    return result


def service_format_phone_num(num):
    """Логика форматирования номера телефона для шаблона"""
    num = str(num)
    return f'{num[0:2]} ({num[2:5]}) {num[5:8]}-{num[8:10]}-{num[10:12]}'
