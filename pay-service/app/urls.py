from django.urls import path
from .views import PaymentViewSet

urlpatterns = [
    path("payments/", PaymentViewSet.as_view(), name="payment-list-create"),
    path("payments/<int:pk>/", PaymentViewSet.as_view(), name="payment-detail"),
]
