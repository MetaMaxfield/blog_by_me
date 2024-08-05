from django.urls import path

from . import views

urlpatterns = [
    # Плоская страница "О нас"
    path('contact/', views.ExtensionFlatpageView.as_view(), name='contact'),
    # URL формы с обратной связью
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
]
