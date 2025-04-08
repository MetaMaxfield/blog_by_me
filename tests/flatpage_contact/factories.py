from django.contrib.flatpages.models import FlatPage
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from flatpage_contact.models import Contact, NewFlatpage


class FlatPageFactory(DjangoModelFactory):
    class Meta:
        model = FlatPage

    url = '/contact/'
    title = 'О нас'
    template_name = 'pages/contact.html'


class NewFlatpageFactory(DjangoModelFactory):
    class Meta:
        model = NewFlatpage

    flatpage = SubFactory(FlatPageFactory)
    google_maps_html = (
        '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d208958.36104585734!2d-106.671984!3d35.08237'
        '26!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87220addd309837b%3A0xc0d3f8ceb8d9f6fd!2z0JDQu9GM0LHRg9C'
        '60LXRgNC60LUsINCd0YzRji3QnNC10LrRgdC40LrQviwg0KHQqNCQ!5e0!3m2!1sru!2sru!4v1743604415820!5m2!1sru!2sru" '
        'width="425" height="360" style="border:0;" allowfullscreen="" loading="lazy" '
        'referrerpolicy="no-referrer-when-downgrade"></iframe>'
    )
    description = 'Описание компании'
    email_contact = Faker('email')
    phone1_num = Faker('phone_number')
    phone2_num = Faker('phone_number')


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = Faker('name')
    email = Faker('email')
    phone = Faker('phone_number')
    message = Faker('sentence', nb_words=10)
