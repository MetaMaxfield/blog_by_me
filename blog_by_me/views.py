from django.contrib import admin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found_view(request: HttpRequest, exception: Http404) -> HttpResponse:
    """
    Представление, которое должно быть вызвано,
    если ни один из шаблонов URL-адресов не совпадает
    """
    return render(request, '404.html', status=404)


# Изменения заголовка и подзаголовка в панеле администрирования
admin.site.index_title = 'Добро пожаловать в панель администрации'
admin.site.site_header = 'Панель администрирования'
admin.site.site_title = 'Панель администрирования'
