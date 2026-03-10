from django.db import models


class Shipment(models.Model):
    METHOD_CHOICES = [
        ("STANDARD", "Giao hàng tiêu chuẩn"),
        ("EXPRESS", "Giao hàng nhanh"),
        ("PICKUP", "Nhận tại cửa hàng"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "Chờ xử lý"),
        ("SHIPPED", "Đã giao"),
        ("DELIVERED", "Đã nhận"),
        ("CANCELLED", "Đã hủy"),
    ]

    order_id = models.IntegerField()
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="STANDARD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "app"

    def __str__(self):
        return f"Shipment #{self.id} - Order {self.order_id} - {self.method} - {self.status}"
