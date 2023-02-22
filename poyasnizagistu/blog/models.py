from django.db import models
from django.urls import reverse
from users.models import CustomUser
from ckeditor_uploader.fields import RichTextUploadingField
def post_directory_path(instance, filename):
    return 'blog/category/{0}/{1}/{2}'.format(instance.cat.slug, instance.slug, filename)
class Post(models.Model):
    title = models.CharField(verbose_name='_____Пост_____', max_length=40, unique=True)
    slug = models.SlugField(max_length=40, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(verbose_name='Фото', upload_to=post_directory_path, blank=True)
    text = models.TextField(verbose_name='Текст')
    time_create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Публикация', default=True)
    cat = models.ForeignKey('Categories_Post', verbose_name='Категория', on_delete=models.PROTECT, null=False)

    thumbsup = models.IntegerField(verbose_name='Нравится', default='0')
    thumbsdown = models.IntegerField(verbose_name='Не нравится', default='0')
    thumbs = models.ManyToManyField(CustomUser, verbose_name='Голосовали', related_name='thumbs', default=None, blank=True)

    def comment_count(self):
        return self.comments_post.all().count()

    comment_count.short_description = 'Комментариев'

    def text_100(self):
        if len(self.text) > 99:
            return u"%s..." % (self.text[:100],)
        else:
            return self.text

    text_100.short_description = '___Текст поста___'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-time_create']


class Votes_Post(models.Model):
    post = models.ForeignKey(Post, related_name='postid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(CustomUser, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)

class Comments_Post(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, verbose_name='Пост', related_name='comments_post' )
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE, verbose_name='Автор комментария', related_name='comments_post_author')
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    text = models.TextField(max_length=700, verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)

    def text_100(self):
        if len(self.text) > 99:
            return u"%s..." % (self.text[:100],)
        else:
            return self.text

    text_100.short_description = 'Текст комментария'


    def __str__(self):
        return f'Пост: {self.post} |  Автор:{self.author}'

    class Meta:
        verbose_name = "Комментарий постa"
        verbose_name_plural = "Комментарии постов"
        ordering = ['-status', '-create_date',]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.post.slug})

class Categories_Post(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=40, db_index=True, unique=True)
    slug = models.SlugField(max_length=80, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"


class HomeHi(models.Model):
    title = models.CharField(verbose_name='Приветствие', max_length=40, unique=True)
    body = RichTextUploadingField(verbose_name='Содержание приветсвия')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        verbose_name = "Одно приветствие"
        verbose_name_plural = "Одно приветствие"
