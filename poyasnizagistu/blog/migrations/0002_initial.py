# Generated by Django 4.1.4 on 2023-02-10 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='votes_post',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.categories_post', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='post',
            name='thumbs',
            field=models.ManyToManyField(blank=True, default=None, related_name='thumbs', to=settings.AUTH_USER_MODEL, verbose_name='Голосовали'),
        ),
        migrations.AddField(
            model_name='comments_post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AddField(
            model_name='comments_post',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_post', to='blog.post', verbose_name='Пост'),
        ),
    ]
