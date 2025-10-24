from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title