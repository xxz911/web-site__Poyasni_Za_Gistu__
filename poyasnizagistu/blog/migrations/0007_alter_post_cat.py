# Generated by Django 4.1.4 on 2023-01-17 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_categorypost_remove_post_likes_alter_post_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.categorypost', verbose_name='Категория'),
        ),
    ]
