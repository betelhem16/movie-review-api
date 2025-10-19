from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
class Review(models.Model):
    movie_title = models.CharField(max_length=200, db_index=True)
    review_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True, db_index=True)
    movie_year = models.CharField(max_length=10, blank=True, null=True)
    movie_genre = models.CharField(max_length=200, blank=True, null=True)
    movie_poster = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['movie_title']), models.Index(fields=['rating'])]
    def __str__(self):
        return f"{self.movie_title} - {self.owner.username}"
