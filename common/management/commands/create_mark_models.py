import logging

from django.core.management import BaseCommand

from blog.models import Mark
from blog_by_me import settings

logger = logging.getLogger(__name__)

MARKS_LIST = [
    {
        'id': 1,
        'nomination_ru': settings.RU_TITLE_DISLIKE_MARK,
        'nomination_en': settings.EN_TITLE_DISLIKE_MARK,
        'value': -1
    },
    {
        'id': 2,
        'nomination_ru': settings.RU_TITLE_LIKE_MARK,
        'nomination_en': settings.EN_TITLE_LIKE_MARK,
        'value': 1
    },
]


class Command(BaseCommand):

    help = 'Создает экземпляры модели Mark для возможности оценивания постов.'

    def handle(self, *args, **options):

        # Цикл создания объектов модели Mark
        for mark in MARKS_LIST:

            self.stdout.write(f'\nСоздание оценки {mark["nomination_ru"]}...')

            # Создание или обновление существующей оценки
            new_mark, created = Mark.objects.update_or_create(
                id=mark['id'],
                nomination_ru=mark['nomination_ru'],
                nomination_en=mark['nomination_en'],
                value=mark['value']
            )

            # Оповещение при создании объекта модели
            if created:
                info = f'Оценка с наименованием "{mark["nomination_ru"]}" создана.'
                self.stdout.write(self.style.SUCCESS(info))

            # Оповещение при обновлении объекта модели
            else:
                info = (
                    f'Оценка с наименованием "{mark["nomination_ru"]}" уже существует. '
                    f'Данные экземпляра модели обновлены.'
                )
                logger.warning(info)
                self.stdout.write(self.style.WARNING(info))
