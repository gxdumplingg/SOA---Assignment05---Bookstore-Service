from django.urls import path

from .views import AddressViewSet, CustomerViewSet


urlpatterns = [
    path("customers/", CustomerViewSet.as_view(), name="customer-list-create"),
    path("customers/<int:pk>/", CustomerViewSet.as_view(), name="customer-detail"),
    path("addresses/", AddressViewSet.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", AddressViewSet.as_view(), name="address-detail"),
]

