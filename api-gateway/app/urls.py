from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_customer, name='register_customer'),
    path('customers/', views.customer_list, name='customer_list'),
    path('orders/', views.order_list, name='order_list'),
    path('select-customer/', views.select_customer, name='select_customer'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/rate/', views.rate_book, name='rate_book'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_id>/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/<int:cart_id>/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('staff/', views.staff_register, name='staff_register'),
    path('staff/books/', views.staff_book_list, name='staff_book_list'),
    path('staff/books/add/', views.staff_book_add, name='staff_book_add'),
    path('staff/books/<int:book_id>/edit/', views.staff_book_edit, name='staff_book_edit'),
    path('staff/books/<int:book_id>/delete/', views.staff_book_delete, name='staff_book_delete'),
]
