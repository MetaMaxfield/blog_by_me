from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from blog_by_me.settings import STATIC_URL
from services.users.validator import username_validator


class CustomUser(AbstractUser):
    """Пользователь"""
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        help_text='Обязательное условие. 150 символов или меньше. '
                  'Только буквы, цифры, пробелы и @/./+/-/_.',
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    description = models.TextField(verbose_name='Информация об пользователе', blank=True)
    image = models.ImageField(
        verbose_name='Изображение пользователя',
        upload_to='users/',
        null=True,
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        verbose_name='Общее количество лайков',
        default=0
    )
    is_staff = models.BooleanField(
        verbose_name='Статус персонала',
        default=True,
        help_text='Определяет, может ли пользователь войти '
                  'на сайт администрирования.',
    )
    email = models.EmailField(verbose_name="E-mail", blank=False)

    def get_image_url(self):
        """Метод проверки наличия изображения у автора"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return STATIC_URL + 'img/comment_icon.png'

    def get_user_groups(self):
        # Метод получения групп пользователя
        try:
            groups = Group.objects.filter(user__id=self.id)
            return [group.name for group in groups]
        except:
            return []
    get_user_groups.short_description = 'Группы пользователя'

    def get_last_posts_user(self):
        # Метод получения трёх последних опубликованных постов пользователя
        return self.post_author.filter(draft=False).select_related(
            'category', 'author'
        ).only(
            'category__name', 'title', 'url', 'body', 'image', 'publish', 'author__id'
        )[:3]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
