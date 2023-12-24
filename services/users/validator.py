from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class ImprovedUnicodeUsernameValidator(validators.RegexValidator):
    """
    Расширенный валидатор для поля "username" модели "CustomUser"
    при создании пользователя, где дополнительно разрешены пробелы
    """
    regex = r'^[ \w.@+-]+\Z'
    message = (
        'Введите допустимое имя пользователя. Это значение может содержать только буквы, '
        'числа, пробелы и @/./+/-/_.'
    )
    flags = 0


username_validator = ImprovedUnicodeUsernameValidator()
