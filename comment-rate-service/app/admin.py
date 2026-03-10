from django.contrib import admin

from .models import BookRating


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_id', 'customer_id', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('book_id', 'customer_id')
