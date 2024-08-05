"""
URL configuration for blog_by_me project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Панель администратора
    path('admin/', admin.site.urls),
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Мультиязычность
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    # Простые страницы
    path('pages/', include('flatpage_contact.urls')),
    # Страницы пользователей
    path('authors/', include('users.urls')),
    # Страницы блога
    path('', include('blog.urls')),
)


# Полный путь импорта Python к представлению, которое должно быть вызвано,
# если ни один из шаблонов URL-адресов не совпадает
handler404 = 'blog_by_me.views.page_not_found_view'


# Отображение панели отладки при включенном "DEBUG" режиме
if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include("debug_toolbar.urls")),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
