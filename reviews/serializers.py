from rest_framework import serializers
from .models import Review
class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Review
        fields = ['id','movie_title','review_text','rating','movie_year','movie_genre','movie_poster','owner','created_at','updated_at']
    def validate_rating(self, value):
        if value is None:
            return value
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
