from django.contrib.flatpages.models import FlatPage
from django.core.management import BaseCommand
from flatpage_contact.models import NewFlatpage


class Command(BaseCommand):
    help = 'Создает плоскую страницу "О нас" с расширенными возможностями'

    def handle(self, *args, **options):
        about_flatpage = FlatPage.objects.create(url='/contact/', title='О нас', template_name='pages/contact.html')
        NewFlatpage.objects.create(flatpage=about_flatpage)
        print('Плоская страница "О нас" с расширенными возможностями создана')
