from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'slug', 'first_name', 'last_name', 'email', 'get_avatar', 'birthday', 'age', 'gender', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'gender', 'date_joined')
    list_filter = ('birthday', 'age', 'gender', 'is_active', 'date_joined', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    prepopulated_fields = {"slug": ('username',)}

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Info',
            {
                'fields': ('slug', 'first_name', 'last_name', 'email', 'get_avatar', 'avatar', 'birthday', 'gender')
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Info',
            {
                'fields': ('slug', 'get_avatar', 'birthday', 'avatar')
            }
        )
    )

    readonly_fields = ('get_avatar', 'last_login', 'date_joined', 'age')

    #   Метод для получения миниатюр
    def get_avatar(self, object):
        return mark_safe(f"<img src='{object.avatar.url}' width=6"f"0>")

    get_avatar.short_description = 'Миниатюра'

