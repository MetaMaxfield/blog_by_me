from django.test import SimpleTestCase
from parameterized import parameterized

from blog_by_me import settings
from services.caching import _get_cache_time


class GetCacheTimeTest(SimpleTestCase):
    """Тестирование функции _get_cache_time"""

    def test_all_cache_keys(self):
        """
        Проверяем, что ключи CACHE_TIMES соответствуют ожидаемому набору.

        Важно: при добавлении новых ключей необходимо обновить
        параметры в test_get_cache_time(_, qs_key, expected_cache_time)
        """
        expected_cache_keys = {
            settings.KEY_POSTS_LIST,
            settings.KEY_POST_DETAIL,
            settings.KEY_CATEGORIES_LIST,
            settings.KEY_VIDEOS_LIST,
            settings.KEY_CONTACT_FLATPAGE,
            settings.KEY_AUTHORS_LIST,
            settings.KEY_AUTHOR_DETAIL,
            settings.KEY_TOP_POSTS,
            settings.KEY_LAST_POSTS,
            settings.KEY_ALL_TAGS,
            settings.KEY_POSTS_CALENDAR,
        }
        self.assertEqual(set(settings.CACHE_TIMES.keys()), expected_cache_keys)

    @parameterized.expand(
        [
            # время кеширования для списка постов
            ('for_posts_list', settings.KEY_POSTS_LIST, 300),
            # время кеширования для отдельного поста
            ('for_post_detail', settings.KEY_POST_DETAIL, 600),
            # время кеширования для списка категорий
            ('for_categories_list', settings.KEY_CATEGORIES_LIST, 3600),
            # время кеширования для списка видеозаписей
            ('for_videos_list', settings.KEY_VIDEOS_LIST, 600),
            # время кеширования для данных страницы "О нас"
            ('for_contact_flatpage', settings.KEY_CONTACT_FLATPAGE, 86400),
            # время кеширования для списка авторов
            ('for_authors_list', settings.KEY_AUTHORS_LIST, 3600),
            # время кеширования для отдельного автора
            ('for_author_detail', settings.KEY_AUTHOR_DETAIL, 600),
            # время кеширования для топа постов
            ('for_top_posts', settings.KEY_TOP_POSTS, 900),
            # время кеширования для последних постов
            ('for_last_posts', settings.KEY_LAST_POSTS, 300),
            # время кеширования для списка с тегами
            ('for_all_tags', settings.KEY_ALL_TAGS, 1800),
            # время кеширования для дней публикации постов
            ('for_posts_calendar', settings.KEY_POSTS_CALENDAR, 3600),
            # время кеширования для не заданных ключей (по умолчанию)
            ('for_unspecified_key', 'UNSPECIFIED_KEY', 300),
        ]
    )
    def test_get_cache_time(self, _, qs_key, expected_cache_time):
        fact_cache_time = _get_cache_time(qs_key)
        self.assertEqual(fact_cache_time, expected_cache_time)
