from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe

from blog.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'cat', 'title', 'get_photo', 'text', 'time_create')
    list_display_links = ('id', 'title', 'get_photo', 'text')
    list_editable = ('is_published', 'cat')
    list_filter = ('time_create', 'is_published', 'cat__name', 'thumbsup', 'thumbsdown')
    fields = ('cat', 'title', 'slug', 'photo', 'get_photo', 'text', 'is_published', 'time_create')
    readonly_fields = ('time_create', 'get_photo')
    search_fields = ('id', 'cat', 'title', 'text', 'time_create')
    prepopulated_fields = {"slug": ('title',)}

    def get_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=6"
                             f"0>")

    get_photo.short_description = 'Фото'



admin.site.register(Post, PostAdmin)


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    fields = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}



admin.site.register(Categories_Post, PostCategoryAdmin)

class CommentsPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'create_date', 'text', 'status')
    list_display_links = ('text',)
    fields = ('post', 'author', 'text', 'status')
    list_editable = ('status',)
    search_fields = ('post', 'author', 'create_date', 'text',)
    list_filter = ('status', 'post__title', 'author__username', 'create_date',)





admin.site.register(Comments_Post, CommentsPostAdmin)
