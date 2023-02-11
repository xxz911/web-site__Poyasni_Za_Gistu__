from django.contrib import admin
from django.utils.safestring import mark_safe

from albums.models import *


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'organ_system', 'title', 'get_cover', 'thumbsup', 'thumbsdown')
    list_display_links = ('id', 'title')
    list_editable = ('is_published', 'organ_system')
    list_filter = ('organ_system__name', 'title', 'is_published', 'thumbsup', 'thumbsdown')
    fields = ('is_published', 'organ_system', 'title', 'cover', 'get_cover', 'slug',)
    readonly_fields = ('get_cover',)
    search_fields = ('id', 'title', 'organ_system')
    prepopulated_fields = {"slug": ('title',)}

    def get_cover(self, object):
        if object.cover:
            return mark_safe(f"<img src='{object.cover.url}' width=6"
                             f"0>")

    get_cover.short_description = 'Миниатюра'




admin.site.register(Album, AlbumAdmin)


class OrganSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    fields = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}



admin.site.register(Organ_System, OrganSystemAdmin)


class CommentsAlbumAdmin(admin.ModelAdmin):
    list_display = ('album', 'author', 'create_date', 'text', 'status')
    list_display_links = ('text',)
    fields = ('album', 'author', 'text', 'status')
    list_editable = ('status',)
    search_fields = ('album', 'author', 'create_date', 'text',)
    list_filter = ('status', 'album__title', 'author__username', 'create_date',)





admin.site.register(Comments_Album, CommentsAlbumAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ('album', 'title_image', 'get_image', 'comment_image', 'title_image_description', 'get_image_description', 'comment_image_description' )
    list_display_links = ('get_image', 'get_image_description', 'title_image', 'title_image_description',)
    fields = ('album', 'title_image', 'image', 'get_image', 'comment_image', 'title_image_description', 'image_description', 'get_image_description', 'comment_image_description', )
    list_editable = ('album',)
    search_fields = ('title_image', 'image', 'comment_image', 'title_image_description', 'image_description', 'comment_image_description', 'album')
    readonly_fields = ('get_image', 'get_image_description',)
    list_filter = ('album__title', 'title_image', 'title_image_description')

    def get_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=6"
                             f"0>")

    get_image.short_description = 'Миниатюра изображения'

    def get_image_description(self, object):
        if object.image_description:
            return mark_safe(f"<img src='{object.image_description.url}' width=6"
                             f"0>")

    get_image_description.short_description = 'Миниатюра изображения с пояснениями'



admin.site.register(Images, ImagesAdmin)