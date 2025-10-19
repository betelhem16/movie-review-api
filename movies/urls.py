# movies/urls.py
from django.urls import path
from .views import DiscoverMoviesView, PopularView, RecommendationsView

urlpatterns = [
    path('discover/', DiscoverMoviesView.as_view(), name='discover'),
    path('popular/', PopularView.as_view(), name='popular'),
    path('<int:tmdb_id>/recommendations/', RecommendationsView.as_view(), name='recommendations'),
]
