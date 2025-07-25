![gif-logo](https://github.com/MetaMaxfield/blog_by_me/raw/master/Blog-by-Me.gif)

<h1>
    <img align="left" src='https://github.com/MetaMaxfield/blog_by_me/raw/master/static/img/site_logo.png?raw=true' width="53.5" height="48.72" alt="logo">
    Блог "MAXFIELD"
</h1>

![Static Badge](https://img.shields.io/badge/Python-3.11-blue?logo=python&labelColor=black)
![Static Badge](https://img.shields.io/badge/Django-4.2-lightgrey?logo=Django&labelColor=darkgreen)
![Static Badge](https://img.shields.io/badge/PostgreSQL-%231f618d?logo=postgresql&logoColor=white)
![Static Badge](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white)
![Static Badge](https://img.shields.io/badge/Memcached-%2316a085)


Полноценный веб-проект с реализованным back-end на Django.

## Содержание:

- [Инструменты](#используемые-технологии-и-инструменты)
- [Функционал](#реализованный-функционал)
- [Особенности](#особенности-проекта)
- [Структура](#структура-проекта-директории-и-файлы)
- [Установка](#установка)
- [Источники](#источники)

## Используемые технологии и инструменты:

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Django 4.2.1](https://docs.djangoproject.com/en/4.2/)
- [PostgreSQL](https://www.postgresql.org/)
- [Memcached](https://memcached.org/)
- [SMTP Gmail](https://myaccount.google.com/apppasswords)
- [Google reCAPTCHA v3](https://www.google.com/recaptcha/admin/create?hl=ru)
- [Docker](https://www.docker.com/)

## Реализованный функционал:

- Система пользователей (Гость, Автор, Модератор, Администратор);
- Панель администратора с разграничением прав доступа по ролям пользователей;
- Система постов с архитектурой блога;
- Категории и теги к постам;
- Фильтрация постов по категориям, тегам и дате публикации;
- Поиск постов по названию или содержанию;
- Постраничное отображение данных;
- Комментарии к постам и ответы к ним;
- Виджеты боковой панели: топ постов, последние записи, календарь публикаций, популярные теги;
- Навигационная цепочка сайта;
- Система рейтинга постов;
- Отложенная публикация постов;
- Собственный видеохостинг проекта;
- Возможность задать вопрос авторам блога с ответом на e-mail;
- Блок "Поделиться" в личных профилях авторов и в записях блога;
- Мультиязычность моделей и страниц (Русский, Английский);
- Защита от интернет-ботов (ReCAPTCHA v3).

## Особенности проекта:

- Представления на базе generic‑классов и View;
- Полнотекстовый поиск на основе векторного сопоставления с ранжированием результатов по релевантности;
- Персонализированные шаблонные теги для логики отображения возраста и виджетов боковой панели;
- Персонализированные шаблонные фильтры для форматирования данных в шаблонах;
- Промежуточное ПО (middleware) для автоматической установки русского языка в панели администратора;
- Использование IP пользователей в системе рейтинга постов;
- Расширенная встроенная модель плоских страниц для хранения дополнительной информации о проекте;
- Поддержка встраиваемой карты Google Maps: местоположение можно изменить напрямую через панель администратора;
- Реализация навигационной цепочки с помощью специализированных шаблонных тегов;
- Страница ошибки 404 с индивидуальным оформлением;
- Интерфейс шаблонов в виде переиспользуемых компонентов и именованных блоков;
- Индивидуальный валидатор для поля модели пользователя;
- Автоудаление неиспользуемых медиафайлов (с помощью сигналов);
- Оптимизация запросов к базе данных;
- Кэширование отдельных данных;
- Получение данных из кэша или БД по ключам из переменных виртуального окружения;
- Расширение функциональности шаблонов панели администрирования;
- Вынесение бизнес-логики в сервисный слой для повышения читаемости и поддержки кода;
- Debug-toolbar для отладки в процессе разработки;
- Логгирование уровней WARNING и ERROR в отдельный файл для отслеживания ошибок в пользовательской логике;
- Пользовательские команды для упрощения рутинных операций и администрирования проекта:
    * Создание расширенной плоской страницы с информацией о веб-проекте;
    * Создание необходимых групп пользователей;
    * Создание оценочных значений для системы рейтинга.
- Линтеры и форматтеры: black, isort, flake8 с настроенными pre-commit хуками;
- Интеграция библиотеки python-dotenv для работы с переменными окружения и хранения приватных параметров проекта;
- Готовые медиафайлы и данные БД для локальной разработки и ручного тестирования;
- Мультиплатформенность за счёт использования Docker для развёртывания базы данных и кэш-сервиса;
- Автоматизированный скрипт для быстрого старта проекта:
    * Создание виртуального окружения;
    * Установка зависимостей;
    * Скачивание, распаковка и последующее удаление медиаархива для ручного тестирования;
    * Создание .env с необходимыми переменными;
    * Настройка pre-commit хуков;
    * Запуск контейнеров с БД и кэшем;
    * Запуск локального сервера.
- Юнит-тесты и интеграционные тесты на unittest с использованием встроенных фикстур, фабрик для генерации тестовых данных и отслеживанием покрытия кода.

## Структура проекта (директории и файлы):
```
├── blog                                    # Пакет с приложением
│   ├── migrations                          # Пакет с миграциями
│   ├── templatetags                        # Пакет с шаблонными тегами и фильтрами для приложения
│   │   └── post_tag.py                     # Файл с шаблонными тегами и фильтрами для приложения
│   ├── admin.py                            # Файл с зарегистрированными моделями приложения в системе администрирования
│   ├── apps.py                             # Файл с конфигурацией приложения
│   ├── forms.py                            # Файл для хранения форм
│   ├── models.py                           # Файл с моделями данных приложения
│   ├── signals.py                          # Файл с обработчиками сигналов приложения
│   ├── translation.py                      # Файл с обозначением полей моделей для локализации
│   ├── urls.py                             # Файл с шаблонами адресов проекта
│   └── views.py                            # Файл с логикой приложения
├── blog_by_me                              # Пакет с файлами проекта
│   ├── asgi.py                             # Файл с конфигурацией для расширения возможностей WSGI
│   ├── middleware.py                       # Файл для плагинов глобального изменения входных и выходных данных
│   ├── settings.py                         # Файл с конфигурацией проекта
│   ├── urls.py                             # Файл с шаблонами адресов приложения 
│   ├── views.py                            # Файл с логикой отдельных функций в проекте
│   └── wsgi.py                             # Файл с конфигурацией для запуска проекта как WSGI-приложения
├── common                                  # Пакет с приложением, файлы которого используются в нескольких других приложениях
│   ├── management                          # Родительский пакет для пакета с файлами пользовательских команд
│   │   └── commands                        # Пакет с файлами пользовательских команд
│   │       ├── create_flatpage_contact.py  # Файл пользовательской команды создания расширенной плоской страницы
│   │       ├── create_groups.py            # Файл пользовательской команды создания групп пользователей
│   │       └── create_mark_models.py       # Файл пользовательской команды создания оценок к постам
│   ├── templatetags                        # Директория с шаблонными тегами и фильтрами для проекта
│   │   ├── breadcrumbs.py                  # Файл шаблонных тегов навигационной цепочки
│   │   └── common_tag.py                   # Файл с шаблонными тегами и фильтрами для проекта
│   └── admin.py                            # Файл с зарегистрированными моделями проекта в системе администрирования
├── db_init                                 # Директория инициализации тестовой базы данных
│   └── backup.sql                          # Файл для инициализации тестовой базы данных
├── flatpage_contact                        # Пакет с приложением
│   ├── migrations                          # Пакет с миграциями
│   ├── templatetags                        # Пакет с шаблонными тегами и фильтрами для приложения
│   │   └── contact_tag.py                  # Файл с шаблонными тегами и фильтрами для приложения
│   ├── admin.py                            # Файл с зарегистрированными моделями приложения в системе администрирования
│   ├── apps.py                             # Файл с конфигурацией приложения
│   ├── forms.py                            # Файл для хранения форм
│   ├── models.py                           # Файл с моделями данных приложения
│   ├── translation.py                      # Файл с обозначением полей моделей для локализации
│   ├── urls.py                             # Файл с шаблонами адресов приложения
│   └── views.py                            # Файл с логикой приложения
├── locale                                  # Директория с локализацией
├── logs                                    # Директория с файлами для логгирования
│   └── user_commands.log                   # Файл с логами ошибок и предупреждений пользовательских команд
├── media                                   # Директория с изображениями и видеофайлами, которые добавляются при создании модели
├── services                                # Пакет с сервисным слоем приложений
│   ├── blog                                # Пакет с сервисным слоем приложения "blog"
│   │   ├── paginator.py                    # Файл с модулем постраничного вывода
│   │   └── video_player.py                 # Файл с модулем видеоплеера
│   ├── flatpage_contact                    # Пакет с сервисным слоем приложения "flatpage_contact"
│   │   └── send_mail.py                    # Файл с модулем отправки сообщений через e-mail
│   ├── users                               # Пакет с сервисным слоем приложения "users"
│   │   └── validator.py                    # Файл с модулем валидатора поля модели приложения
│   ├── caching.py                          # Файл с модулем кэширования
│   ├── client_ip.py                        # Файл с модулем получения ip пользователя
│   ├── queryset.py                         # Файл с модулем чтения данных из базы данных
│   ├── rating.py                           # Файл с модулем добавления рейтинга
│   ├── search.py                           # Файл с модулем поиска
│   └── template_tags.py                    # Файл с модулем шаблонных тегов и фильтров
├── static                                  # Директория для хранения статических файлов
├── templates                               # Директория для хранения структуры HTML-шаблонов
├── tests                                   # Пакет с тестами проекта
│   ├── blog                                # Пакет с тестами приложения "blog"
│   │   ├── factories.py                    # Файл с фабриками моделей
│   │   ├── test_forms.py                   # Файл с тестами форм
│   │   └── test_models.py                  # Файл с тестами моделей
│   ├── flatpage_contact                    # Пакет с тестами приложения "flatpage_contact"
│   │   ├── factories.py                    # Файл с фабриками моделей
│   │   ├── test_forms.py                   # Файл с тестами форм
│   │   └── test_models.py                  # Файл с тестами моделей
│   ├── services                            # Пакет с тестами сервисного слоя
│   │   ├── blog                            # Пакет с тестами сервисного слоя приложения "blog"
│   │   │   └──test_paginator.py            # Файл с тестами модуля постраничного вывода
│   │   ├── flatpage_contact                # Пакет с тестами сервисного слоя приложения "flatpage_contact"
│   │   │   └──test_send_mail.py            # Файл с тестами модуля отправки сообщений через e-mail
│   │   ├── users                           # Пакет с тестами сервисного слоя приложения "users"
│   │   │   └──test_validator.py            # Файл с тестами модуля валидатора поля модели приложения
│   │   ├── test_caching.py                 # Файл с тестами модуля кэширования
│   │   ├── test_client_ip.py               # Файл с тестами модуля получения ip пользователя
│   │   ├── test_queryset.py                # Файл с тестами модуля чтения данных из базы данных
│   │   ├── test_rating.py                  # Файл с тестами модуля добавления рейтинга
│   │   ├── test_search.py                  # Файл с тестами модуля поиска
│   │   └── test_template_tags.py           # Файл с тестами модуля шаблонных тегов и фильтров
│   └── users                               # Пакет с тестами приложения "users"
│       ├── factories.py                    # Файл с фабриками моделей
│       ├── test_models.py                  # Файл с тестами моделей
│       └── test_views.py                   # Файл с тестами представлений
├── users                                   # Пакет с приложением
│   ├── migrations                          # Пакет с миграциями
│   ├── templatetags                        # Пакет с шаблонными тегами и фильтрами для приложения
│   │   └── users_tag.py                    # Файл с шаблонными тегами и фильтрами для приложения
│   ├── admin.py                            # Файл с зарегистрированными моделями приложения в системе администрирования
│   ├── apps.py                             # Файл с конфигурацией приложения
│   ├── models.py                           # Файл с моделями данных приложения
│   ├── signals.py                          # Файл с обработчиками сигналов приложения
│   ├── translation.py                      # Файл с обозначением полей моделей для локализации
│   ├── urls.py                             # Файл с шаблонами адресов приложения 
│   └── views.py                            # Файл с логикой приложения
├── .env                                    # Файл с переменными окружения (добавляется через запуск setup_dev.py)
├── .gitattributes                          # Файл с атрибутами Git
├── .gitignore                              # Файл для списка файлов и папок, которые Git игнорирует и не отслеживает
├── .pre-commit-config.yaml                 # Файл конфигурации для настройки хуков pre-commit
├── Blog-by-Me.gif                          # GIF-изображение с логотипом проекта
├── docker-compose.yaml                     # Файл конфигурации для запуска контейнеров
├── manage.py                               # Файл-утилита командной строки для управления проектом
├── pyproject.toml                          # Файл конфигурации для форматера кода black
├── README.md                               # Файл с руководством описания проекта
├── requirements.txt                        # Файл с названиями модулей и пакетов для корректной работы проекта
├── setup.cfg                               # Файл конфигурации для линтера кода flake8 и организатора импортов isort
└── setup_dev.py                            # Скрипт-файл для старта локальной разработки
```

## Установка:

1. Копируем содержимое репозитория (требуется установленный [Git](https://git-scm.com/downloads))

    ```
    git clone https://github.com/MetaMaxfield/blog_by_me.git
    ```
   
2. Добавляем проект в приложения Google аккаунта и сохраняем пароль приложения

3. Регистрируем сайт на Google ReCAPTCHA, сохраняем ключ сайта и секретный ключ

4. Запускаем Docker Desktop

5. Выполним автоматическую подготовку проекта к локальной разработке

    - Запускаем через консоль файл setup_dev.py
      ```
      python setup_dev.py
      ```
   
   - В процессе настройки переменных окружения нужно добавить следующие значения:
   
     Пример: ``` SECRET_KEY=your_secret_key ```

     ```
     # Список переменных окружения, значения которых мы сохраняли ранее:
     EMAIL_HOST_USER_KEY=         # Почта Google аккаунта для отправки e-mail 
     EMAIL_HOST_PASSWORD_KEY=     # Пароль от приложения из Google аккаунта
     ENV_RECAPTCHA_PUBLIC_KEY=    # Ключ сайта из Google ReCAPTCHA
     ENV_RECAPTCHA_PRIVATE_KEY=   # Секретный ключ из Google ReCAPTCHA
     KEY_DATABASES_USER=          # Имя пользователя в PostgreSQL
     KEY_DATABASES_PASSWORD=      # Пароль пользователя в PostgreSQL
     ```
     
6. Проект готов к локальной разработке. Локальный сервер запущен автоматически.

## Источники:
1. [Документация Python 3.11](https://docs.python.org/3.11/)
2. [Документация Django 4.2](https://docs.djangoproject.com/en/4.2/)
3. [Онлайн-инспектор для Class‑Based Views](https://ccbv.co.uk/)
4. [Документация Docker](https://docs.docker.com/reference/)
5. [Справочник по HTML](https://htmlbook.ru/html)
6. [Руководство по тестированию](https://developer.mozilla.org/ru/docs/Learn_web_development/Extensions/Server-side/Django/Testing)
7. Книга "Django 2 в примерах" А. Меле
8. [YouTube канал "Михаил Омельченко"](https://www.youtube.com/@DjangoSchool)
9. [ChatGPT-4o от OpenAI](https://chatgpt.com/)
10. [Готовый HTML шаблон](http://html-template.ru/blogi/item/289-modnyj-i-sovremennyj-blog)