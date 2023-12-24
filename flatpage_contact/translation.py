from modeltranslation.translator import register, TranslationOptions
from .models import NewFlatpage


@register(NewFlatpage)
class NewFlatpageTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('description', )