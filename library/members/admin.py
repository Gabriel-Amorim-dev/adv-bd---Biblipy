# members/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member


@admin.register(Member)
class MemberAdmin(UserAdmin):

    list_display = (
        'username',
        'registration_number',
        'full_name',
        'email',
        'phone',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'registration_number',
        'full_name',
        'email',
    )

    list_filter = (
        'is_staff',
        'is_active',
        'is_superuser',
    )

    ordering = ('username',)

    list_per_page = 10

    fieldsets = UserAdmin.fieldsets + (
        ('Library Information', {
            'fields': (
                'registration_number',
                'full_name',
                'phone',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Library Information', {
            'fields': (
                'full_name',
                'phone',
            )
        }),
    )