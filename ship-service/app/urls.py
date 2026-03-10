from django.urls import path
from .views import ShipmentViewSet

urlpatterns = [
    path("shipments/", ShipmentViewSet.as_view(), name="shipment-list-create"),
    path("shipments/<int:pk>/", ShipmentViewSet.as_view(), name="shipment-detail"),
]
