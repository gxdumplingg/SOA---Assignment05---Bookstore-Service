from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BookRating(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'app'
        constraints = [
            models.UniqueConstraint(fields=['customer_id', 'book_id'], name='uniq_customer_book_rating')
        ]

    def __str__(self) -> str:
        return f"Rating {self.rating}/5 - book {self.book_id} - customer {self.customer_id}"
