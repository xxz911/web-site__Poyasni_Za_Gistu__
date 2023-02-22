from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from slugify import slugify
from django.urls import reverse


def user_directory_path(instance, filename):
    return 'users/avatar/{0}/{1}'.format(instance.slug,filename)

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
                                upload_to=user_directory_path, blank=True, )
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDERS, default='-', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст',null=True,  blank=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_slug': self.slug})

    def save(self, *args, **kwargs,):
        if not self.slug:
            self.slug = slugify(self.username)
        if not self.age and self.birthday:
            birthday = self.birthday
            today = date.today()
            age = str(today - birthday)
            self.age = int(int(age.split()[0])/360)
        if self.age and self.birthday:
            birthday = self.birthday
            today = date.today()
            age = str(today - birthday)
            self.age = int(int(age.split()[0])/360)

        return super().save(*args, **kwargs)

