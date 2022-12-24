from django.db import models


class Post(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    photo = models.ImageField(verbose_name='Фото', upload_to="blog/photo/", blank=True)
    text = models.TextField(verbose_name='Текст', blank=True)
    time_create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Публикация', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
