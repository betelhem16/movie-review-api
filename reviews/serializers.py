from rest_framework import serializers
from .models import Review, Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'tmdb_id', 'title', 'year', 'genres', 'poster', 'overview']

class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = MovieSerializer(read_only=True)
    movie_title = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'movie', 'movie_title', 'review_text', 'rating',
            'movie_year', 'movie_genre', 'movie_poster',
            'owner', 'created_at', 'updated_at'
        ]
        read_only_fields = ['movie', 'owner', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value is None:
            return value
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value