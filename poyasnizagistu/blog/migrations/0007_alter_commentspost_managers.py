# Generated by Django 4.1.4 on 2023-01-21 22:53

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_commentspost_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='commentspost',
            managers=[
                ('custom_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
