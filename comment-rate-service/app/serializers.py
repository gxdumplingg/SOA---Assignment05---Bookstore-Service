from rest_framework import serializers

from .models import BookRating


class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = [
            'id',
            'customer_id',
            'book_id',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
