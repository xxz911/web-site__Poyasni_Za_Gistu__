# Generated by Django 4.1.4 on 2023-01-21 22:39

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_commentspost_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='commentspost',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
