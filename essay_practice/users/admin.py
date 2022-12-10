from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Profile


class ProfileMoreInfo(BaseUserAdmin):
    model = Profile
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}),
        (
            ('Персональная информация'),
            {'fields': ('username', 'first_name', 'last_name')}
        ),
        (
            ('Права доступа'),
            {'fields': (
                'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )}
        ),
        (
            ('Важные даты'),
            {'fields': ('last_login', 'date_joined')}
        ),
    )


admin.site.register(Profile, ProfileMoreInfo)
