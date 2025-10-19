from django.contrib import admin
from .models import Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie_title','owner','rating','created_at')
    search_fields = ('movie_title','owner__username')
    list_filter = ('rating',)
