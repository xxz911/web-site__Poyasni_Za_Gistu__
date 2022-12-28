from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_avatar', 'age', 'gender', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'age', 'gender', 'date_joined')
    list_filter = ('age', 'gender', 'is_active', 'date_joined', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Info',
           {
              'fields': ('first_name', 'last_name', 'email','get_avatar', 'avatar', 'age', 'gender')
           }
        )
     )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Info',
            {
                'fields': ('get_avatar', 'avatar')
            }
        )
     )

    readonly_fields = ('get_avatar', 'last_login', 'date_joined')
    def get_avatar(self, object):
        return mark_safe(f"<img src='{object.avatar.url}' width=6"
                             f"0>")
    get_avatar.short_description = 'Аватар'