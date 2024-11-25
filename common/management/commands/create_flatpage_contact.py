import logging

from django.contrib.flatpages.models import FlatPage
from django.core.management import BaseCommand

from flatpage_contact.models import NewFlatpage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Создает плоскую страницу "О нас" с расширенными возможностями.'

    def handle(self, *args, **options):
        if NewFlatpage.objects.exists():
            info = 'Плоская страница "О нас" с расширенными возможностями уже существует.'
            logger.error(info)
            self.stdout.write(self.style.ERROR(info))
        else:
            info = 'Плоская страница "О нас" с расширенными возможностями создана.'
            about_flatpage = FlatPage.objects.create(url='/contact/', title='О нас', template_name='pages/contact.html')
            NewFlatpage.objects.create(flatpage=about_flatpage)
            self.stdout.write(self.style.SUCCESS(info))
