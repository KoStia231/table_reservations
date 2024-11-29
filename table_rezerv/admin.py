from django.contrib import admin
from table_rezerv.models import Table, Reservation


@admin.register(Table)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'detailed_info')
    search_fields = ('id', 'status', 'number')
    list_filter = ('id', 'status', 'number')


@admin.register(Reservation)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'detailed_info')
    search_fields = ('id', 'status', 'table', 'customer', 'date', 'time', 'duration', 'end_time')
    list_filter = ('id', 'status', 'table', 'customer', 'date', 'time', 'duration', 'end_time')
