from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Info',
           {
              'fields': ('first_name', 'last_name', 'email', 'avatar', 'age', 'gender')
           }
        )
     )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Info',
            {
                'fields': ('avatar',)
            }
        )
     )

