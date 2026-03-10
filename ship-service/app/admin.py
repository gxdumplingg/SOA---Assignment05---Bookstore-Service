from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "method", "status", "created_at")
    list_filter = ("status", "method")
    search_fields = ("order_id",)
