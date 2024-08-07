from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from flatpage_contact.models import Contact, NewFlatpage


class DescriptionAdminForm(forms.ModelForm):
    """Ckeditor для поля "description" расширенной модели плоской страницы"""

    description_ru = forms.CharField(label='Основной текстовый контент страницы [ru]', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Основной текстовый контент страницы [en]', widget=CKEditorUploadingWidget())

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


@admin.register(NewFlatpage)
class FlatpageContactAdmin(TranslationAdmin):
    """Плоская страница"""

    form = DescriptionAdminForm
    fieldsets = (
        (
            'Местонахождение проекта',
            {
                'description': 'Выбрать объект на карте -> Поделиться -> '
                'Встраивание карт -> Другой размер -> 425x360 -> '
                'Копировать HTML',
                'fields': ('google_maps_html',),
            },
        ),
        ('О проекте', {'fields': ('description',)}),
        ('Электронная почта для связи', {'fields': ('email_contact',)}),
        ('Телефоны для связи', {'description': 'Пример: +79099099900', 'fields': (('phone1_num', 'phone2_num'),)}),
    )
