from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Post(models.Model):
    title = models.CharField(verbose_name='Название', max_length=40, unique=True)
    slug = models.SlugField(max_length=40, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(verbose_name='Фото', upload_to="blog/photo/", blank=True)
    text = models.TextField(verbose_name='Текст')
    time_create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Публикация', default=True)
    cat = models.ForeignKey('CategoryPost', verbose_name='Категория', on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-time_create', 'title']


class CommentsPost(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, verbose_name='Пост', related_name='comments_post' )
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE, verbose_name='Автор комментария', related_name='comments_author')
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=700, verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)

    def __str__(self):
        return f'Пост: {self.post} |  Автор:{self.author}'

    class Meta:
        verbose_name = "Комментарий постa"
        verbose_name_plural = "Комментарии постов"
        ordering = ['-status', '-create_date',]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.post.slug})

class CategoryPost(models.Model):
    name = models.CharField(verbose_name='Название', max_length=40, db_index=True, unique=True)
    slug = models.SlugField(max_length=80, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"