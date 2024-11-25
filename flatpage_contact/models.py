from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class NewFlatpage(models.Model):
    """Расширенная плоская страница"""

    flatpage = models.OneToOneField(FlatPage, on_delete=models.CASCADE)
    google_maps_html = models.TextField(verbose_name='HTML-код Google Maps', default='')
    description = models.TextField(verbose_name='Основной текстовый контент страницы', default='')
    email_contact = models.EmailField(verbose_name='Эл. почта для контакта', default='')
    phone1_num = PhoneNumberField(verbose_name='Мобильный телефон')
    phone2_num = PhoneNumberField(verbose_name='Стационарный телефон')

    def __str__(self):
        return self.flatpage.title

    def save(self, *args, **kwargs):
        if not self.pk and NewFlatpage.objects.exists():
            raise ValidationError('Нельзя создать более одного экземпляра модели NewFlatpage.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Содержание страницы'
        verbose_name_plural = 'Содержание страницы'


class Contact(models.Model):
    """Обратная связь"""

    name = models.CharField(verbose_name='Имя')
    email = models.EmailField(verbose_name='Эл. почта')
    phone = PhoneNumberField(verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now_add=True)
    feedback = models.BooleanField(verbose_name='Обрантая связь', default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Запрос от пользователя блога'
        verbose_name_plural = 'Запросы от пользователей блога'
