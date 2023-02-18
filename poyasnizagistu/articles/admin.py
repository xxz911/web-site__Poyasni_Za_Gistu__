from django.contrib import admin

from articles.models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'thematic', 'title', 'time_create', 'thumbsup', 'thumbsdown')
    list_display_links = ('id', 'title')
    list_editable = ('is_published', 'thematic')
    list_filter = ('time_create', 'is_published', 'thematic__name', 'thumbsup', 'thumbsdown')
    fields = ('thematic', 'title', 'body', 'slug', 'is_published', 'time_create')
    readonly_fields = ('time_create', )
    search_fields = ('id', 'thematic', 'title', 'time_create')
    prepopulated_fields = {"slug": ('title',)}




admin.site.register(Article, ArticleAdmin)


class ArticleThematicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    fields = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}



admin.site.register(Thematic, ArticleThematicAdmin)

class CommentsArticleAdmin(admin.ModelAdmin):
    list_display = ('status', 'text', 'article', 'author', 'create_date')
    list_display_links = ('text',)
    fields = ('article', 'author', 'text', 'status')
    list_editable = ('status',)
    search_fields = ('article', 'author', 'create_date', 'text',)
    list_filter = ('status', 'article__title', 'author__username', 'create_date',)




admin.site.register(Comments_Article, CommentsArticleAdmin)

