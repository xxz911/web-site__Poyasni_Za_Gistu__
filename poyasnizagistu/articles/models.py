from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from users.models import CustomUser



class Article(models.Model):
    title = models.CharField(verbose_name='Статья', max_length=40, unique=True)
    slug = models.SlugField(max_length=40, unique=True, db_index=True, verbose_name='URL')

    body = RichTextUploadingField(verbose_name='Содержание')

    time_create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Публикация', default=True)
    thematic = models.ForeignKey('Thematic', verbose_name='Тематика', on_delete=models.PROTECT, null=False)

    thumbsup = models.IntegerField(verbose_name='Нравится', default='0')
    thumbsdown = models.IntegerField(verbose_name='Не нравится', default='0')
    thumbs = models.ManyToManyField(CustomUser, verbose_name='Голосовали', related_name='thumbs_article', default=None, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"
        ordering = ['-time_create']

class Votes_Article(models.Model):
    article = models.ForeignKey(Article, related_name='articleid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(CustomUser, related_name='userarticleid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)


class Comments_Article(models.Model):
    article = models.ForeignKey(Article, on_delete= models.CASCADE, verbose_name='Название Статьи', related_name='comments_article' )
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE, verbose_name='Автор комментария', related_name='comments_article_author')
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    text = models.TextField(max_length=700, verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)

    def __str__(self):
        return f'Статья: {self.article} |  Автор:{self.author}'

    class Meta:
        verbose_name = "Комментарий статьи"
        verbose_name_plural = "Комментарии статей"
        ordering = ['-status', '-create_date',]

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.article.slug})

class Thematic(models.Model):
    name = models.CharField(verbose_name='Тематика', max_length=40, db_index=True, unique=True)
    slug = models.SlugField(max_length=80, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('thematic', kwargs={'thematic_slug': self.slug})

    class Meta:
        verbose_name = "Тематику"
        verbose_name_plural = "Тематики"