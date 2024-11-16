from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering=['email']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        for fieldset in fieldsets:
            if 'fields' in fieldset[1]:
                fieldset[1]['fields'] = [field for field in fieldset[1]['fields'] if field != 'username']
        return fieldsets
