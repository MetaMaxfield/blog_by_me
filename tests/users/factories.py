from factory.django import DjangoModelFactory

from users.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = 'Maximus'
    description = 'Описание пользователя'
    email = 'maximus@gmail.com'
