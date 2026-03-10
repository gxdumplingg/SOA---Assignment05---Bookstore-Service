from django.contrib import admin

from .models import Address, Customer, FullName


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")


@admin.register(FullName)
class FullNameAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "full_name")
    search_fields = ("full_name",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "line1", "city", "is_default")
    list_filter = ("is_default",)
    search_fields = ("line1", "city", "customer__email")
