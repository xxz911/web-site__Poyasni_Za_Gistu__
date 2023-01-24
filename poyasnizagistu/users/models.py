from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from slugify import slugify
from django.urls import reverse



class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'


    GENDERS = (
        ('', 'Не указано'),
        ('М', 'Мужчина'),
        ('Ж', 'Женщина'),
    )
    slug = models.SlugField(max_length=40, unique=True, db_index=True, verbose_name='URL')
    avatar = models.ImageField(verbose_name='Аватар', default='users/avatar/default/default_avatar.jpeg',
                                upload_to='users/avatar/', blank=True, )
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDERS, default='-', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', blank=True,
                                default=0,
                                validators=[
                                            MaxValueValidator(101),

                                 ]
                                )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)

        return super().save(*args, **kwargs)

