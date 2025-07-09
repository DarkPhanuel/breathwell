from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import PasswordResetToken, User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone', 'is_admin', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
        ('Alert Settings', {'fields': ('pollution_threshold', 'receive_alerts')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_admin', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    readonly_fields = ('token', 'created_at', 'expires_at')

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True


admin.site.register(User, UserAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
admin.site.unregister(Group)