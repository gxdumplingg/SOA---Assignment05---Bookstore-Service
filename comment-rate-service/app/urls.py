from django.urls import path

from .views import RatingViewSet, RatingsByBook, RatingsByCustomer

urlpatterns = [
    path('ratings/', RatingViewSet.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingViewSet.as_view(), name='rating-detail'),
    path('ratings/book/<int:book_id>/', RatingsByBook.as_view(), name='ratings-by-book'),
    path('ratings/customer/<int:customer_id>/', RatingsByCustomer.as_view(), name='ratings-by-customer'),
]
