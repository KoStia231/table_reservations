from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'email')
    search_fields = ('id', 'name', 'phone_number', 'email')
    list_filter = ('id', 'name', 'phone_number', 'email')
