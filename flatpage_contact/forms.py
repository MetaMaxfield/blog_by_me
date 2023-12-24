from django import forms
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from django.conf import settings
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from .models import Contact


class ContactForm(forms.ModelForm):
    """Форма для обратной связи на плоской странице"""
    captcha = ReCaptchaField(
        widget=ReCaptchaV3, public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA'
    )

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'message', 'captcha')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'span10', 'data-required': 'true'}
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'span10',
                    'data-required': 'true',
                    'data-type': 'email'
                }
            ),
            'phone': RegionalPhoneNumberWidget(
                attrs={
                    'class': 'span10',
                    'data-trigger': 'keyup',
                    'data-type': 'phone'
                }
            ),
            'message': forms.Textarea(attrs={'class': 'span10', 'data-trigger': 'keyup'}),
        }