from django.contrib import admin

from main.models import (
    SiteText, SiteImage,
    Staff, Services, Feedback
)


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


@admin.register(Staff)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'job_title',)
    search_fields = ('id', 'name', 'job_title',)
    list_filter = ('id', 'name', 'job_title',)


@admin.register(Services)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('id', 'title',)
    list_filter = ('id', 'title',)


@admin.register(Feedback)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')
    search_fields = ('id', 'name', 'email', 'phone')
    list_filter = ('id', 'name', 'email', 'phone')
