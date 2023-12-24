import os
from django.shortcuts import redirect, render
from django.views import View
from flatpage_contact.forms import ContactForm
from dotenv import load_dotenv
from services.caching import get_cached_objects_or_queryset
from services.flatpage_contact.send_mail import send


load_dotenv()


class ExtensionFlatpageView(View):
    """Плоская страница"""
    def get(self, request):
        contact_flatpage = get_cached_objects_or_queryset(os.getenv('KEY_CONTACT_FLATPAGE'))
        form = ContactForm()
        return render(
            request, 'pages/contact.html', {
                'form': form,
                'flatpage': contact_flatpage
            }
        )


class FeedbackView(View):
    """Обратная связь"""
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            send(form.instance.email)
        return redirect('contact')
