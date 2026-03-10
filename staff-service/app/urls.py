from django.urls import path

from .views import StaffViewSet


urlpatterns = [
    path("staff/", StaffViewSet.as_view(), name="staff-list-create"),
    path("staff/<int:pk>/", StaffViewSet.as_view(), name="staff-detail"),
]

