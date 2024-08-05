from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms
from django.conf import settings

from .models import Comment, Mark, Rating


class CommentsForm(forms.ModelForm):
    """Форма добавления комментариев"""

    captcha = ReCaptchaField(
        widget=ReCaptchaV3,
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        label='ReCAPTCHA',
    )

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span10', 'data-required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'span10', 'data-required': 'true', 'data-type': 'email'}),
            'text': forms.Textarea(attrs={'class': 'span10', 'data-trigger': 'keyup', 'id': 'contactcomment'}),
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""

    rating_captcha = ReCaptchaField(
        widget=ReCaptchaV3,
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        label='ReCAPTCHA',
    )
    mark = forms.ModelChoiceField(
        queryset=Mark.objects.all().order_by('-value'), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('mark', 'rating_captcha')
