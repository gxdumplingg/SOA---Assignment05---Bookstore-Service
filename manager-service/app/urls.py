from django.urls import path

from .views import ManagerViewSet


urlpatterns = [
    path("managers/", ManagerViewSet.as_view(), name="manager-list-create"),
    path("managers/<int:pk>/", ManagerViewSet.as_view(), name="manager-detail"),
]

