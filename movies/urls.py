# movies/urls.py
from django.urls import path
from .views import MovieListView, DiscoverMoviesView, PopularView, RecommendationsView

urlpatterns = [
     path('', MovieListView.as_view(), name='movie-list'),

    path('discover/', DiscoverMoviesView.as_view(), name='discover'),
    path('popular/', PopularView.as_view(), name='popular'),
    path('<int:tmdb_id>/recommendations/', RecommendationsView.as_view(), name='recommendations'),
]
