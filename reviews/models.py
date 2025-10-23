from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)  # comma separated
    poster = models.URLField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    movie_title = models.CharField(max_length=200, db_index=True)
    review_text = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movie_title} by {self.owner.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')
