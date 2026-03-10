from rest_framework import serializers

class RecommendedBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    title = serializers.CharField()
    score = serializers.FloatField()