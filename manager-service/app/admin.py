from django.contrib import admin

from .models import Manager


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "level", "department", "is_active")
    list_filter = ("is_active", "department", "level")
    search_fields = ("name", "email", "level", "department")
