import os, requests
from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Review, Movie
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from movies.tmdb import search_movie, get_movie_details, poster_url, get_genre_mapping
TMDB_API_KEY = os.getenv('TMDB_API_KEY', None)
TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
TMDB_DETAILS_URL = 'https://api.themoviedb.org/3/movie/{}'
def fetch_tmdb_info(title):
    if not TMDB_API_KEY:
        return None
    try:
        params = {'api_key': TMDB_API_KEY, 'query': title}
        r = requests.get(TMDB_SEARCH_URL, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            results = data.get('results') or []
            if results:
                top = results[0]
                movie_id = top.get('id')
                r2 = requests.get(TMDB_DETAILS_URL.format(movie_id), params={'api_key': TMDB_API_KEY}, timeout=5)
                if r2.status_code == 200:
                    d = r2.json()
                    genre_names = [g['name'] for g in d.get('genres', [])]
                    poster_path = d.get('poster_path')
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                    return {'year': d.get('release_date','')[:4] if d.get('release_date') else None,'genre': ', '.join(genre_names) if genre_names else None,'poster': poster_url}
    except requests.RequestException:
        return None
    return None
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating']
    search_fields = ['movie_title', 'review_text']
    ordering_fields = ['rating', 'created_at']
    def get_queryset(self):
        queryset = super().get_queryset()
        movie = self.request.query_params.get('movie', None)
        if movie:
            queryset = queryset.filter(movie_title__icontains=movie)
        return queryset
    def perform_create(self, serializer):
        title = serializer.validated_data.get('movie_title')
        movie = get_or_create_movie_by_title(title)
        serializer.save(owner=self.request.user, movie=movie)
       
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
def home_view(request):
    latest = Review.objects.all()[:10]
    return render(request, 'reviews/index.html', {'reviews': latest})
def get_or_create_movie_by_title(title):
    existing = Movie.objects.filter(title__iexact=title).first()
    if existing:
        return existing

    search = search_movie(title)
    if search and search.get("results"):
        top = search["results"][0]
        tmdb_id = top.get("id")
        movie, created = Movie.objects.get_or_create(tmdb_id=tmdb_id, defaults={
            "title": top.get("title") or title,
            "year": (top.get("release_date") or "")[:4],
            "overview": top.get("overview") or ""
        })
        # fetch details
        details = get_movie_details(tmdb_id)
        if details:
            genres = ", ".join([g['name'] for g in details.get('genres', [])])
            p = poster_url(details.get('poster_path'))
            movie.year = (details.get('release_date') or "")[:4] or movie.year
            movie.genres = genres or movie.genres
            movie.poster = p or movie.poster
            movie.overview = details.get('overview') or movie.overview
            movie.title = details.get('title') or movie.title
            movie.save()
        return movie

    # fallback - create a local movie with only title
    return Movie.objects.create(title=title)
