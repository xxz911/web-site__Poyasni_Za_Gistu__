# Generated by Django 4.1.4 on 2023-01-05 21:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(110), django.core.validators.MinValueValidator(14)], verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]