from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from blog_by_me.settings import TITLE_MODERATOR_GROUP, TITLE_AUTHOR_GROUP
import logging

GROUPS = {
    TITLE_AUTHOR_GROUP: {
        'Категория': ['add', 'change', 'view'],
        'Комментарий': ['view', ],
        'Пост': ['add', 'delete', 'change', 'view'],
        'Рейтинг': ['view', ],
        'Видеозапись': ['add', 'delete', 'change', 'view'],
        'Пользователь': ['change', ],
        'Запрос от пользователя блога': ['view', ],
        'tag': ['add', 'view'],
        'tagged item': ['add', 'view'],
    },

    TITLE_MODERATOR_GROUP: {
        'Категория': ['add', 'delete', 'change', 'view'],
        'Комментарий': ['add', 'delete', 'change', 'view'],
        'Пост': ['add', 'delete', 'change', 'view'],
        'Рейтинг': ['view', ],
        'Видеозапись': ['add', 'delete', 'change', 'view'],
        'Запрос от пользователя блога': ['view', 'delete'],
        'Содержание страницы': ['add', 'delete', 'change', 'view'],
        'Пользователь': ['view', ],
        'tag': ['add', 'delete', 'change', 'view'],
        'tagged item': ['add', 'delete', 'change', 'view'],
    },
}


class Command(BaseCommand):
    help = "Создает группы с разрешениями для пользователей"

    def handle(self, *args, **options):

        # Цикл групп в списке
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)

            # Цикл моделей в группах
            for app_model in GROUPS[group_name]:

                # Цикл разрешений в моделях групп
                for permission_name in GROUPS[group_name][app_model]:

                    # Создание названия разрешения Django.
                    name = f"Can {permission_name} {app_model}"
                    print(f'Создание разрешения {name}')

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning(f'Разрешение с именем "{name}" не найдено')
                        continue

                    new_group.permissions.add(model_add_perm)
