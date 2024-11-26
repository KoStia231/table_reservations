from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')
    search_fields = ('id', 'name', 'phone', 'email')
    list_filter = ('id', 'name', 'phone', 'email')
