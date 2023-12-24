from modeltranslation.translator import register, TranslationOptions
from .models import CustomUser
from django.contrib.auth.models import Group


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('description',)


@register(Group)
class GroupTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('name',)