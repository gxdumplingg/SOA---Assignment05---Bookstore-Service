from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BookRating
from .serializers import BookRatingSerializer


class RatingViewSet(APIView):
    def get(self, request, pk=None):
        if pk is None:
            qs = BookRating.objects.all().order_by('-created_at')
            serializer = BookRatingSerializer(qs, many=True)
            return Response(serializer.data)

        try:
            obj = BookRating.objects.get(pk=pk)
        except BookRating.DoesNotExist:
            return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookRatingSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        """Upsert theo (customer_id, book_id)."""
        customer_id = request.data.get('customer_id')
        book_id = request.data.get('book_id')
        if customer_id is None or book_id is None:
            return Response({'detail': 'customer_id and book_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = BookRating.objects.get(customer_id=customer_id, book_id=book_id)
            serializer = BookRatingSerializer(obj, data=request.data, partial=True)
        except BookRating.DoesNotExist:
            serializer = BookRatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            obj = BookRating.objects.get(pk=pk)
        except BookRating.DoesNotExist:
            return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookRatingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            obj = BookRating.objects.get(pk=pk)
        except BookRating.DoesNotExist:
            return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookRatingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = BookRating.objects.get(pk=pk)
        except BookRating.DoesNotExist:
            return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RatingsByBook(APIView):
    def get(self, request, book_id):
        qs = BookRating.objects.filter(book_id=book_id).order_by('-created_at')
        serializer = BookRatingSerializer(qs, many=True)
        return Response(serializer.data)


class RatingsByCustomer(APIView):
    def get(self, request, customer_id):
        qs = BookRating.objects.filter(customer_id=customer_id).order_by('-created_at')
        serializer = BookRatingSerializer(qs, many=True)
        return Response(serializer.data)
