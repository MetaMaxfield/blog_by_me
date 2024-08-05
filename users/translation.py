from modeltranslation.translator import TranslationOptions, register

from .models import CustomUser


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('description',)
