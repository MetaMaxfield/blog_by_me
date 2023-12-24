from modeltranslation.translator import register, TranslationOptions
from .models import Category, Video, Post, Mark


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('name', 'description')


@register(Video)
class VideoTranslationsOption(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('title', 'description')


@register(Post)
class PostTranslationsOption(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('title', 'body')


@register(Mark)
class MarkTranslationsOption(TranslationOptions):
    """Мультиязычность выбранных полей"""
    fields = ('nomination', )