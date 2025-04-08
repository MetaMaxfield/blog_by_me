from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory

from users.models import CustomUser


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = 'Модератор'


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = 'Maximus'
    description = 'Описание пользователя'
    email = 'maximus@gmail.com'
