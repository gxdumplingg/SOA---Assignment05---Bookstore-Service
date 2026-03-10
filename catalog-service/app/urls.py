from django.urls import path

from .views import CategoryViewSet


urlpatterns = [
    path("categories/", CategoryViewSet.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryViewSet.as_view(), name="category-detail"),
]

