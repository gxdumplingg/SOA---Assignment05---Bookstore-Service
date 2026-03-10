from django.urls import path

from .views import OrderViewSet, OrderItemListCreateView


urlpatterns = [
    path("orders/", OrderViewSet.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderViewSet.as_view(), name="order-detail"),
    path("orders/<int:order_id>/items/", OrderItemListCreateView.as_view(), name="orderitem-list-create"),
]

