from django.test import SimpleTestCase

from services import queryset


class NotDefiniteQSTest(SimpleTestCase):
    """Тестирование функции not_definite_qs"""

    def test_not_definite_qs(self):
        # Проверка №1. Проверка на вызов ошибки
        with self.assertRaises(Exception) as error:
            queryset.not_definite_qs()

        # Проверка №2. Проверка текста с содержанием ошибки
        expected_message_error = 'Ключ для получения queryset не найден.'
        self.assertEqual(str(error.exception), expected_message_error)
