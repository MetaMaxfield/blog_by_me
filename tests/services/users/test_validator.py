import re

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from parameterized import parameterized

from services.users.validator import username_validator


class ImprovedUnicodeUsernameValidatorTest(SimpleTestCase):
    """Тестирование валидатора ImprovedUnicodeUsernameValidator"""

    def test_regex(self):
        fact_regex = username_validator.regex
        self.assertEqual(fact_regex, re.compile('^[ \\w.@+-]+\\Z'))

    def test_message(self):
        fact_message = username_validator.message
        expected_message = (
            'Введите допустимое имя пользователя. '
            'Это значение может содержать только буквы, числа, пробелы и @/./+/-/_.'
        )
        self.assertEqual(fact_message, expected_message)

    def test_flags(self):
        fact_flags = username_validator.flags
        self.assertEqual(fact_flags, 0)

    @parameterized.expand(
        [
            ('john_doe', True),  # допускаются латинские буквы, подчёркивание
            ('alice.smith', True),  # допускаются латинские буквы, точка
            ('michael+dev', True),  # допускаются латинские буквы, плюс
            ('User 123', True),  # допускаются латинские буквы, пробел, цифры
            ('русский_юзер', True),  # допускаются кириллица, подчёркивание
            ('invalid|name', False),  # не допускается символ "|"
            ('name<alert>', False),  # не допускаются символы "<" и ">"
            ('hello/world', False),  # не допускается символ "/"
            ('bad"name', False),  # не допускаются кавычки
            ('tricky\\name', False),  # не допускается обратный слэш "\"
        ]
    )
    def test_validate_username(self, username, is_valid_expected):
        try:
            username_validator(username)
            self.assertTrue(is_valid_expected, f'Валидатор ошибочно принял: "{username}"')
        except ValidationError:
            self.assertFalse(is_valid_expected, f'Валидатор ошибочно отклонил: "{username}"')
