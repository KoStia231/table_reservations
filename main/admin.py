from django.contrib import admin

from main.models import SiteText, SiteImage


@admin.register(SiteText)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'key',)
    search_fields = ('id', 'key',)
    list_filter = ('id', 'key',)


@admin.register(SiteImage)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'key',)
    search_fields = ('id', 'key',)
    list_filter = ('id', 'key',)
