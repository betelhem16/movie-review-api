from rest_framework import serializers
from .models import Review, Movie, Like

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','tmdb_id','title','year','genres','poster','overview']

class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = MovieSerializer(read_only=True)
    movie_title = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = ['id','movie','movie_title','review_text','rating','owner','created_at','updated_at','likes_count']

    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    def validate_rating(self, value):
        if value is None:
            return value
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        if not data.get('movie_title'):
            raise serializers.ValidationError({'movie_title': 'This field is required.'})
        if not data.get('review_text'):
            raise serializers.ValidationError({'review_text': 'This field is required.'})
        return data

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = ['id','user','review','created_at']
