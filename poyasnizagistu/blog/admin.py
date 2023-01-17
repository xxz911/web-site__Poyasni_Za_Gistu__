from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('cat', 'id', 'title', 'get_photo', 'text', 'time_create', 'is_published')
    list_display_links = ('id', 'title', 'get_photo')
    list_editable = ('is_published', 'cat')
    list_filter = ('time_create', 'is_published')
    fields = ('cat', 'title', 'photo', 'get_photo', 'text', 'is_published', 'time_create')
    readonly_fields = ('time_create', 'get_photo')
    search_fields = ('cat', 'id', 'title', 'photo', 'text', 'time_create')

    def get_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=6"
                             f"0>")

    get_photo.short_description = 'Фото'



admin.site.register(Post, PostAdmin)
admin.site.register(CategoryPost)


