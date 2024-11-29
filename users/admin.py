from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'detailed_info')
    search_fields = ('id', 'name', 'phone', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('id', 'name', 'phone', 'email', 'is_active', 'is_staff', 'is_superuser')
