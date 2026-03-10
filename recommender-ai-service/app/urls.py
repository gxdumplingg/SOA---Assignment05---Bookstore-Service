from django.urls import path
from .views import RecommendView

urlpatterns = [
    path("recommendations/", RecommendView.as_view(), name="recommend-list"),
    path("recommendations/<int:customer_id>/", RecommendView.as_view(), name="recommend-for-customer"),
]