from django.contrib.auth.models import Group
from factory import Sequence
from factory.django import DjangoModelFactory

from users.models import CustomUser


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = 'Модератор'


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = Sequence(lambda n: f'Maximus{n + 1}')
    description = 'Описание пользователя'
    email = Sequence(lambda n: f'maximus{n + 1}@gmail.com')
