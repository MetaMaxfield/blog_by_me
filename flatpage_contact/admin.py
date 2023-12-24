from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django import forms
from .models import *
from modeltranslation.admin import TranslationStackedInline


class DescriptionAdminForm(forms.ModelForm):
    """Ckeditor для поля "description" расширенной модели плоской страницы"""
    description_ru = forms.CharField(
        label='Основной текстовый контент страницы',
                                     widget=CKEditorUploadingWidget()
    )
    description_en = forms.CharField(
        label='Основной текстовый контент страницы',
                                     widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = NewFlatpage
        fields = '__all__'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Обратная связь"""
    list_display = ('name', 'email', 'phone', 'date', 'feedback')
    list_filter = ('email', 'phone')
    search_fields = ('name', 'email', 'phone')
    list_editable = ('feedback',)
    readonly_fields = ('name', 'email', 'phone', 'date', 'message')


class NewFlatpageInline(TranslationStackedInline):
    """
    Отображение новых полей расширенной модели плоской страницы
    в панеле администрации
    """
    model = NewFlatpage
    verbose_name = 'Содержание'
    form = DescriptionAdminForm
    fieldsets = (
        ('О проекте', {
            'fields': ('description', )
        }),
        ('Электронная почта для связи', {
            'fields': ('email_contact', )
        }),
        ('Телефоны для связи', {
            'description': 'Пример: +79099099900',
            'fields': (('phone1_num', 'phone2_num'), )
        }),
    )


class FlatPageNewAdmin(FlatPageAdmin):
    """Плоская страница"""
    inlines = [NewFlatpageInline]
    fieldsets = (
        (None, {'fields': ('url', 'title', 'sites')}),
        (('Advanced options'), {
            'fields': ('template_name',),
        }),
    )
    list_display = ('title', 'url')
    list_display_links = ('title',)
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')


# Регистрация расширенной модели плоской страницы
# для отображения в панели администрации
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageNewAdmin)