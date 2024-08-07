import os

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from dotenv import load_dotenv

from flatpage_contact.forms import ContactForm
from services.caching import get_cached_objects_or_queryset
from services.flatpage_contact.send_mail import send

load_dotenv()


class ExtensionFlatpageView(View):
    """Плоская страница"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            'pages/contact.html',
            {'form': ContactForm(), 'flatpage': get_cached_objects_or_queryset(os.getenv('KEY_CONTACT_FLATPAGE'))},
        )


class FeedbackView(View):
    """Обратная связь"""

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            send(form.instance.email)
        return redirect('contact')
