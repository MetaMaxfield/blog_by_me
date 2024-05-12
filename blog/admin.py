from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from modeltranslation.admin import TranslationAdmin
from .models import Post, Category, Comment, Video, Mark, Rating
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from blog_by_me.settings import TITLE_MODERATOR_GROUP


# Зарегистрированная модель Comment для отображения в панели администрациии
admin.site.register(Comment)


class PostAdminForm(forms.ModelForm):
    """Ckeditor для поля "body" модели блога"""
    body_ru = forms.CharField(
        label='Содержание [ru]',
        widget=CKEditorUploadingWidget()
    )
    body_en = forms.CharField(
        label='Содержание [en]',
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentInline(admin.TabularInline):
    """
    Отображение комментариев на странице записи
    блога в панеле администрации
    """
    model = Comment
    extra = 1


@admin.register(Mark)
class MarkAdmin(TranslationAdmin):
    """Оценки"""
    list_display = ('nomination', 'value')
    list_display_links = ('nomination',)


@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    """Видео"""
    list_display = ('title', 'file', 'create_at')
    list_display_links = ('title',)
    list_filter = ('title',)
    ordering = ('title', 'create_at')
    search_fields = ('title',)

    def get_queryset(self, request):
        # Получение видео из базы данных в зависимости от статуса пользователя
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            try:
                request.user.groups.get(name=TITLE_MODERATOR_GROUP)
                return qs
            except:
                return qs.filter(post_video__author=request.user)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ('name', 'description', 'url')
    list_display_links = ('name',)
    prepopulated_fields = {'url': ('name',)}
    list_filter = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    """Посты"""
    list_display = [
        'id', 'title', 'url', 'author',
        'publish', 'draft', 'get_image'
    ]
    list_editable = ('draft',)
    list_filter = ('title', 'author', 'category', 'publish', 'draft')
    list_display_links = ('title',)
    search_fields = ('title', 'body')
    readonly_fields = ['get_image', ]
    prepopulated_fields = {'url': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('draft', 'publish')
    save_on_top = True
    save_as = True
    inlines = [CommentInline, ]
    form = PostAdminForm
    fieldsets = (
        ('Заголовок', {
            'fields': ('title', )
        }),
        ('Категория', {
            'fields': ('category', 'author')
        }),
        ('Содержание', {
            'fields': ('body', ('image', 'get_image', ), 'video', 'tags', )
        }),
        ('Настройки', {
            'fields': (('draft', 'url'), )
        }),
    )

    def get_image(self, obj):
        # Отображение изображения в панеле администрации
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100", height="100"')
        return 'Нет изображения'
    get_image.short_description = 'Изображение'

    def get_queryset(self, request):
        # Получение постов из базы данных в зависимости от статуса пользователя
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            try:
                request.user.groups.get(name=TITLE_MODERATOR_GROUP)
                return qs
            except:
                return qs.filter(author=request.user)

    def get_fieldsets(self, request, obj=None):
        # Отображение полей в зависимости от статуса пользователя
        fieldsets = super(PostAdmin, self).get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets
        else:
            try:
                request.user.groups.get(name=TITLE_MODERATOR_GROUP)
                return fieldsets
            except:
                fieldsets[1][1]['fields'] = ['category', ]
                return fieldsets

    def save_model(self, request, obj, form, change):
        # Приравнивание полю "Автор" текущего пользователя по умолчанию при сохранении поста
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ['ip', 'mark', 'post']
    search_fields = ['ip', ]
    readonly_fields = ['ip', 'mark', 'post']
    list_filter = ['post', ]
