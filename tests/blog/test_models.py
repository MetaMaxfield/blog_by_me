from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from django.db.models import CASCADE, SET_NULL, Index
from django.test import TestCase
from django.utils import timezone
from taggit.models import Tag

from blog.models import Category, Comment, Mark, Post, Video
from blog_by_me.settings import LANGUAGE_CODE


class CategoryModelTest(TestCase):
    """Тестирование модели Category"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Наука', description='Категория о науке', url='science')

    @classmethod
    def setUp(cls):
        cls.category = Category.objects.get(name='Наука')

    def test_name_verbose_name(self):
        fact_verbose_name = self.category._meta.get_field('name').verbose_name
        self.assertEqual(fact_verbose_name, 'Категория')

    def test_name_max_length(self):
        fact_max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(fact_max_length, 150)

    def test_description_verbose_name(self):
        fact_verbose_name = self.category._meta.get_field('description').verbose_name
        self.assertEqual(fact_verbose_name, 'Описание')

    def test_url_max_length(self):
        fact_max_length = self.category._meta.get_field('url').max_length
        self.assertEqual(fact_max_length, 160)

    def test_url_unique(self):
        fact_unique = self.category._meta.get_field('url').unique
        self.assertTrue(fact_unique)

    def test_object_name_is_name(self):
        expected_object_name = self.category.name
        self.assertEqual(str(self.category), expected_object_name)

    def test_model_verbose_name(self):
        fact_verbose_name = self.category._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Категория')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.category._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Категории')


class VideoModelTest(TestCase):
    """Тестирование модели Video"""

    @classmethod
    def setUpTestData(cls):
        Video.objects.create(
            title='Котята',
            description='Забавные котята',
            file=SimpleUploadedFile("cats.mp4", b"fake video content", content_type="video/mp4"),
        )

    @classmethod
    def setUp(cls):
        cls.video = Video.objects.get(title='Котята')

    def test_title_max_lenght(self):
        fact_max_length = self.video._meta.get_field('title').max_length
        self.assertEqual(fact_max_length, 100)

    def test_title_verbose_name(self):
        fact_verbose_name = self.video._meta.get_field('title').verbose_name
        self.assertEqual(fact_verbose_name, 'Заголовок видео')

    def test_description_verbose_name(self):
        fact_verbose_name = self.video._meta.get_field('description').verbose_name
        self.assertEqual(fact_verbose_name, 'Описание видео')

    def test_file_upload_to(self):
        fact_upload_to = self.video._meta.get_field('file').upload_to
        self.assertEqual(fact_upload_to, 'video/')

    def test_file_validators(self):
        fact_validators = self.video._meta.get_field('file').validators
        self.assertEqual(fact_validators, [FileExtensionValidator(allowed_extensions=['mp4'])])

    def test_file_verbose_name(self):
        fact_verbose_name = self.video._meta.get_field('file').verbose_name
        self.assertEqual(fact_verbose_name, 'Видеофайл')

    def test_create_at_auto_now_add(self):
        fact_auto_now_add = self.video._meta.get_field('create_at').auto_now_add
        self.assertTrue(fact_auto_now_add)

    def test_object_name_is_title(self):
        expected_object_name = self.video.title
        self.assertEqual(str(self.video), expected_object_name)

    def test_model_ordering(self):
        fact_ordering = self.video._meta.ordering
        self.assertEqual(fact_ordering, ('-create_at',))

    def test_model_verbose_name(self):
        fact_verbose_name = self.video._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Видеозапись')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.video._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Видеозаписи')


class PostModelTest(TestCase):
    """Тестирование модели Post"""

    @classmethod
    def setUpTestData(cls):
        author = get_user_model().objects.create(
            username='Maximus', description='Описание пользователя', email='maximus@gmail.com'
        )
        category = Category.objects.create(name='Развлечения', description='Описание категории', url='entertainment')

        cls.post = Post.objects.create(
            title='Как я провёл отпуск',
            url='kak-ya-provel-otpusk',
            author=author,
            category=category,
            body='Содержание событий в отпуске',
            image=SimpleUploadedFile("fishing.jpeg", b"fake image content", content_type="image/jpeg"),
        )

    @classmethod
    def setUp(cls):
        cls.post = Post.objects.get(title='Как я провёл отпуск')

    def test_title_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('title').verbose_name
        self.assertEqual(fact_verbose_name, 'Заголовок')

    def test_title_max_length(self):
        fact_max_length = self.post._meta.get_field('title').max_length
        self.assertEqual(fact_max_length, 250)

    def test_url_max_length(self):
        fact_max_length = self.post._meta.get_field('url').max_length
        self.assertEqual(fact_max_length, 25)

    def test_url_unique(self):
        fact_unique = self.post._meta.get_field('url').unique
        self.assertTrue(fact_unique)

    def test_author_to_model(self):
        fact_to_model = self.post._meta.get_field('author').remote_field.model
        self.assertEqual(fact_to_model, get_user_model())

    def test_author_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('author').verbose_name
        self.assertEqual(fact_verbose_name, 'Автор')

    def test_author_on_delete(self):
        fact_on_delete = self.post._meta.get_field('author').remote_field.on_delete
        self.assertEqual(fact_on_delete, CASCADE)

    def test_author_related_name(self):
        fact_related_name = self.post._meta.get_field('author').remote_field.related_name
        self.assertEqual(fact_related_name, 'post_author')

    def test_category_to_model(self):
        fact_to_model = self.post._meta.get_field('category').remote_field.model
        self.assertEqual(fact_to_model, Category)

    def test_category_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('category').verbose_name
        self.assertEqual(fact_verbose_name, 'Категория')

    def test_category_related_name(self):
        fact_related_name = self.post._meta.get_field('category').remote_field.related_name
        self.assertEqual(fact_related_name, 'post_category')

    def test_category_on_delete(self):
        fact_on_delete = self.post._meta.get_field('category').remote_field.on_delete
        self.assertEqual(fact_on_delete, SET_NULL)

    def test_tags_to_model(self):
        fact_to_model = self.post._meta.get_field('tags').remote_field.model
        self.assertEqual(fact_to_model, Tag)

    def test_tags_related_name(self):
        fact_related_name = self.post._meta.get_field('tags').remote_field.related_name
        self.assertEqual(fact_related_name, 'post_tags')

    def test_body_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('body').verbose_name
        self.assertEqual(fact_verbose_name, 'Содержание')

    def test_video_to_model(self):
        fact_to_model = self.post._meta.get_field('video').remote_field.model
        self.assertEqual(fact_to_model, Video)

    def test_video_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('video').verbose_name
        self.assertEqual(fact_verbose_name, 'Видео к записи')

    def test_video_related_name(self):
        fact_related_name = self.post._meta.get_field('video').remote_field.related_name
        self.assertEqual(fact_related_name, 'post_video')

    def test_video_on_delete(self):
        fact_on_delete = self.post._meta.get_field('video').remote_field.on_delete
        self.assertEqual(fact_on_delete, SET_NULL)

    def test_video_null(self):
        fact_null = self.post._meta.get_field('video').null
        self.assertTrue(fact_null)

    def test_video_blank(self):
        fact_blank = self.post._meta.get_field('video').blank
        self.assertTrue(fact_blank)

    def test_image_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('image').verbose_name
        self.assertEqual(fact_verbose_name, 'Изображение')

    def test_image_upload_to(self):
        fact_upload_to = self.post._meta.get_field('image').upload_to
        self.assertEqual(fact_upload_to, 'posts/')

    def test_publish_default(self):
        fact_default = self.post._meta.get_field('publish').default
        self.assertEqual(fact_default, timezone.now)

    def test_publish_help_text(self):
        fact_help_text = self.post._meta.get_field('publish').help_text
        expected_help_text = (
            'Укажите дату и время, когда пост должен быть опубликован. '
            'Оставьте текущую дату и время для немедленной публикации, '
            'либо выберите будущую дату для отложенного поста. '
            'Обратите внимание: изменить время публикации можно будет только '
            'до наступления ранее указанного времени.'
        )
        self.assertEqual(fact_help_text, expected_help_text)

    def test_publish_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('publish').verbose_name
        self.assertEqual(fact_verbose_name, 'Время публикации')

    def test_created_auto_now_add(self):
        fact_auto_now_add = self.post._meta.get_field('created').auto_now_add
        self.assertTrue(fact_auto_now_add)

    def test_updated_auto_now(self):
        fact_auto_now = self.post._meta.get_field('updated').auto_now
        self.assertTrue(fact_auto_now)

    def test_draft_default(self):
        fact_default = self.post._meta.get_field('draft').default
        self.assertFalse(fact_default)

    def test_draft_verbose_name(self):
        fact_verbose_name = self.post._meta.get_field('draft').verbose_name
        self.assertEqual(fact_verbose_name, 'Черновик')

    def test_object_name_is_title(self):
        expected_object_name = self.post.title
        self.assertEqual(str(self.post), expected_object_name)

    def test_get_absolute_url(self):
        fact_url = self.post.get_absolute_url()
        expected_url = f'/{LANGUAGE_CODE}/{self.post.url}/'
        self.assertEquals(fact_url, expected_url)

    def test_get_comment(self):
        comment1 = Comment.objects.create(
            post=self.post, name='Комментатор 1', email='com1@gmail.com', text='Текст комментария 1'
        )
        Comment.objects.create(
            post=self.post, name='Комментатор 2', email='com2@gmail.com', text='Текст комментария 2', active=False
        )
        Comment.objects.create(
            post=self.post, name='Комментатор 3', email='com3@gmail.com', text='Ответ на комментарий 1', parent=comment1
        )

        # проверка фильтров в тестируемом методе
        fact_comments_to_post = self.post.get_comment()
        expected_comments_to_post = [
            comment1,
        ]
        self.assertQuerySetEqual(fact_comments_to_post, expected_comments_to_post)

        # проверка что для дочерних комментариев используется предзагрузка через .prefetch_related()
        for comment in fact_comments_to_post:
            self.assertIn('parent_comments', getattr(comment, '_prefetched_objects_cache', {}))

    def test_model_verbose_name(self):
        fact_verbose_name = self.post._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Пост')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.post._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Посты')

    def test_model_indexes(self):
        fact_indexes = self.post._meta.indexes
        expected_indexes = [
            Index(fields=('-publish', '-id'), name='publish_id_idx'),
        ]
        self.assertEqual(fact_indexes, expected_indexes)

    def test_model_ordering(self):
        fact_ordering = self.post._meta.ordering
        self.assertEqual(fact_ordering, ('-publish', '-id'))


class CommentModelTest(TestCase):
    """Тестирование модели Comment"""

    @classmethod
    def setUpTestData(cls):
        author = get_user_model().objects.create(
            username='Maximus', description='Описание пользователя', email='maximus@gmail.com'
        )
        category = Category.objects.create(name='Развлечения', description='Описание категории', url='entertainment')
        post = Post.objects.create(
            title='Как я провёл отпуск',
            url='kak-ya-provel-otpusk',
            author=author,
            category=category,
            body='Содержание событий в отпуске',
            image=SimpleUploadedFile("fishing.jpeg", b"fake image content", content_type="image/jpeg"),
        )
        cls.comment = Comment.objects.create(
            post=post, name='Комментатор 1', email='com1@gmail.com', text='Текст комментария 1'
        )
        Comment.objects.create(
            post=post, name='Комментатор 2', email='com2@gmail.com', text='Ответ на комментарий 1', parent=cls.comment
        )

    @classmethod
    def setUp(cls):
        cls.comment = Comment.objects.get(name='Комментатор 1')

    def test_post_to_model(self):
        fact_to_model = self.comment._meta.get_field('post').remote_field.model
        self.assertEqual(fact_to_model, Post)

    def test_post_verbose_name(self):
        fact_verbose_name = self.comment._meta.get_field('post').verbose_name
        self.assertEqual(fact_verbose_name, 'Запись')

    def test_post_on_delete(self):
        fact_on_delete = self.comment._meta.get_field('post').remote_field.on_delete
        self.assertEqual(fact_on_delete, CASCADE)

    def test_post_related_name(self):
        fact_related_name = self.comment._meta.get_field('post').remote_field.related_name
        self.assertEqual(fact_related_name, 'comments')

    def test_parent_model_to(self):
        fact_model_to = self.comment._meta.get_field('parent').remote_field.model
        self.assertEqual(fact_model_to, Comment)

    def test_parent_verbose_name(self):
        fact_verbose_name = self.comment._meta.get_field('parent').verbose_name
        self.assertEqual(fact_verbose_name, 'Родитель')

    def test_parent_on_delete(self):
        fact_on_delete = self.comment._meta.get_field('parent').remote_field.on_delete
        self.assertEqual(fact_on_delete, SET_NULL)

    def test_parent_blank(self):
        fact_blank = self.comment._meta.get_field('parent').blank
        self.assertTrue(fact_blank)

    def test_parent_null(self):
        fact_null = self.comment._meta.get_field('parent').null
        self.assertTrue(fact_null)

    def test_parent_related_name(self):
        fact_related_name = self.comment._meta.get_field('parent').remote_field.related_name
        self.assertEqual(fact_related_name, 'parent_comments')

    def test_name_verbose_name(self):
        fact_verbose_name = self.comment._meta.get_field('name').verbose_name
        self.assertEqual(fact_verbose_name, 'Имя')

    def test_name_max_length(self):
        fact_max_length = self.comment._meta.get_field('name').max_length
        self.assertEqual(fact_max_length, 80)

    def test_text_verbose_name(self):
        fact_verbose_name = self.comment._meta.get_field('text').verbose_name
        self.assertEqual(fact_verbose_name, 'Содержание комментария')

    def test_text_max_length(self):
        fact_max_length = self.comment._meta.get_field('text').max_length
        self.assertEqual(fact_max_length, 5000)

    def test_created_auto_now_add(self):
        fact_auto_now_add = self.comment._meta.get_field('created').auto_now_add
        self.assertTrue(fact_auto_now_add)

    def test_updated_auto_now(self):
        fact_auto_now = self.comment._meta.get_field('updated').auto_now
        self.assertTrue(fact_auto_now)

    def test_active_default(self):
        fact_default = self.comment._meta.get_field('active').default
        self.assertTrue(fact_default)

    def test_object_name_is_name_and_post(self):
        expected_object_name = f'Комментарий от {self.comment.name} к {self.comment.post}'
        self.assertEqual(str(self.comment), expected_object_name)

    def test_model_verbose_name(self):
        fact_verbose_name = self.comment._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Комментарий')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.comment._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Комментарии')

    def test_model_ordering(self):
        fact_ordering = self.comment._meta.ordering
        self.assertEqual(fact_ordering, ('created',))


class MarkModelTest(TestCase):
    """Тестирование модели Mark"""

    @classmethod
    def setUpTestData(cls):
        Mark.objects.create(nomination='Лайк', value=1)

    @classmethod
    def setUp(cls):
        cls.mark = Mark.objects.get(nomination='Лайк')

    def test_nomination_verbose_name(self):
        fact_verbose_name = self.mark._meta.get_field('nomination').verbose_name
        self.assertEqual(fact_verbose_name, 'Наименование')

    def test_nomination_max_length(self):
        fact_max_length = self.mark._meta.get_field('nomination').max_length
        self.assertEqual(fact_max_length, 10)

    def test_value_verbose_name(self):
        fact_verbose_name = self.mark._meta.get_field('value').verbose_name
        self.assertEqual(fact_verbose_name, 'Значение')

    def test_value_default(self):
        fact_default = self.mark._meta.get_field('value').default
        self.assertEqual(fact_default, 0)

    def test_object_name_is_nomination(self):
        expected_object_name = self.mark.nomination
        self.assertEqual(str(self.mark), expected_object_name)

    def test_model_verbose_name(self):
        fact_verbose_name = self.mark._meta.verbose_name
        self.assertEqual(fact_verbose_name, 'Значение рейтинга')

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = self.mark._meta.verbose_name_plural
        self.assertEqual(fact_verbose_name_plural, 'Значения рейтинга')

    def test_model_ordering(self):
        fact_ordering = self.mark._meta.ordering
        self.assertEqual(fact_ordering, ('value',))
