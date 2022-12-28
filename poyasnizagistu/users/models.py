from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'


    GENDERS = (
        ('М', 'Мужчина'),
        ('Ж', 'Женщина'),
    )

    avatar = models.ImageField(verbose_name='Аватар', default='users/avatar/default/default_avatar.jpeg',
                                upload_to='users/avatar/', blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDERS, default='-', blank=True)
    age = models.IntegerField(verbose_name='Возраст', blank=True,
                                default=0,
                                validators=[
                                            MaxValueValidator(110),
                                            MinValueValidator(0)
                                 ]
                                )
    # email = models.EmailField(_("email address"), blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username



