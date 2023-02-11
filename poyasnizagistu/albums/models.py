from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Album(models.Model):
    title = models.CharField(verbose_name='Альбом', max_length=40, unique=True)
    cover = models.ImageField(verbose_name='Обложка', upload_to="album/",)
    slug = models.SlugField(max_length=40, unique=True, db_index=True, verbose_name='URL')
    is_published = models.BooleanField(verbose_name='Публикация', default=True)

    organ_system = models.ForeignKey('Organ_System', verbose_name='Система органов', on_delete=models.CASCADE, null=False)

    thumbsup = models.IntegerField(verbose_name='Нравится', default='0')
    thumbsdown = models.IntegerField(verbose_name='Не нравится', default='0')
    thumbs = models.ManyToManyField(CustomUser, verbose_name='Голосовали', related_name='thumbs_album', default=None, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.slug})


    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ['-title']


class Votes_Album(models.Model):
    album = models.ForeignKey(Album, related_name='albumid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(CustomUser, related_name='useralbumid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)

class Images(models.Model):
    album = models.ForeignKey('Album', related_name='albumimages', verbose_name='Альбом', on_delete=models.CASCADE)
    title_image = models.CharField(verbose_name='Название изображения', max_length=60, unique=True)
    image = models.ImageField(verbose_name='Изображение', upload_to="album/",)
    comment_image = models.CharField(verbose_name='Комментарий изображения', max_length=40)
    title_image_description = models.CharField(verbose_name='Название изображения с пояснениями', max_length=60, unique=True)
    image_description = models.ImageField(verbose_name='Изображение с пояснениями', upload_to="album/",)
    comment_image_description = models.CharField(verbose_name='Комментарий изображения с пояснениями', max_length=40)

    def __str__(self):
        return F'Альбом : {self.album} Изображения: {self.title_image}, {self.title_image_description} '

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.album.slug})

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

class Comments_Album(models.Model):
    album = models.ForeignKey(Album, on_delete= models.CASCADE, verbose_name='Название Альбома', related_name='comments_album' )
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE, verbose_name='Автор комментария', related_name='comments_album')
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    text = models.TextField(max_length=700, verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)

    def __str__(self):
        return f'Альбом: {self.album} |  Автор:{self.author}'

    class Meta:
        verbose_name = "Комментарий альбома"
        verbose_name_plural = "Комментарии альбомов"
        ordering = ['-status', '-create_date',]

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.album.slug})

class Organ_System(models.Model):
    name = models.CharField(verbose_name='Система органов', max_length=40, db_index=True, unique=True)
    slug = models.SlugField(max_length=80, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organ', kwargs={'organ_slug': self.slug})

    class Meta:
        verbose_name = "Систему органов"
        verbose_name_plural = "Системы органов"
