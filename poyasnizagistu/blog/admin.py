from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Count
from blog.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'cat', 'title', 'get_photo', 'text_100', 'time_create', 'thumbsup', 'thumbsdown', 'comments')
    list_display_links = ('id', 'title', 'get_photo', 'text_100')
    list_editable = ('is_published', 'cat')
    list_filter = ('time_create', 'is_published', 'cat__name', 'thumbsup', 'thumbsdown')
    fields = ('cat', 'title', 'slug', 'photo', 'get_photo', 'text', 'is_published', 'time_create', 'thumbsup', 'thumbsdown', 'comments')
    readonly_fields = ('time_create', 'get_photo', 'comments', 'thumbsup', 'thumbsdown')
    search_fields = ('id', 'cat', 'title', 'text', 'time_create', 'comments')
    prepopulated_fields = {"slug": ('title',)}

    def comments(self, obj):
        return obj.comments_count

    comments.short_description = 'Комментариев'
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comments_count=Count("comments_post"))
        return queryset
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
    list_display = ('post', 'author', 'create_date', 'text_100', 'status')
    list_display_links = ('text_100',)
    fields = ('post', 'author', 'text', 'status')
    list_editable = ('status',)
    search_fields = ('post', 'author', 'create_date', 'text',)
    list_filter = ('status', 'post__title', 'author__username', 'create_date',)





admin.site.register(Comments_Post, CommentsPostAdmin)

class HomeHiAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    fields = ('title', 'body',)






admin.site.register(HomeHi, HomeHiAdmin)


admin.site.site_title = 'Администрирование сайта "Поясни за Гисту"'
admin.site.site_header = 'Администрирование сайта "Поясни за Гисту"'