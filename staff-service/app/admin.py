from django.contrib import admin

from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role", "department", "is_active")
    list_filter = ("is_active", "department", "role")
    search_fields = ("name", "email", "role", "department")
