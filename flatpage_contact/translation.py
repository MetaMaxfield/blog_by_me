from modeltranslation.translator import TranslationOptions, register

from .models import NewFlatpage


@register(NewFlatpage)
class NewFlatpageTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('description',)
