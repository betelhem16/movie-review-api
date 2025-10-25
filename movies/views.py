

# Create your views here.
# movies/views.py
from rest_framework import generics, filters
from .models import Movie
from .serializers import MovieSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .tmdb import discover_movies, tmdb_get, get_genre_mapping, poster_url

class DiscoverMoviesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = request.query_params.get('page', 1)
        sort_by = request.query_params.get('sort', 'popularity.desc')
        genre_name = request.query_params.get('genre')
        region = request.query_params.get('region')
        original_lang = request.query_params.get('original_language')

        genre_id = None
        if genre_name:
            mapping = get_genre_mapping()
            # Flip the mapping: name → id
            reverse_mapping = {v.lower(): k for k, v in mapping.items()}
            genre_id = reverse_mapping.get(genre_name.lower())

        data = discover_movies(
            page=page,
            sort_by=sort_by,
            genre_id=genre_id,
            region=region,
            with_original_language=original_lang
        )

        if data is None:
            return Response({"results": []})
        return Response(data)
class PopularView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        page = request.query_params.get('page', 1)
        data = tmdb_get("/movie/popular", {"page": page}, cache_key=f"tmdb_popular_{page}", cache_timeout=60*30)
        return Response(data or {"results": []})

class RecommendationsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, tmdb_id):
        data = tmdb_get(f"/movie/{tmdb_id}/recommendations", cache_key=f"tmdb_recs_{tmdb_id}", cache_timeout=60*30)
        return Response(data or {"results": []})
class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genres']
    filterset_fields = ['year', 'genres']
    ordering_fields = ['release_date', 'title']
class ImportMovieView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        title = request.data.get("title")
        if not title:
            return Response({"error": "Missing 'title' in request body"}, status=400)

        movie = get_or_create_movie_by_title(title)
        if not movie:
            return Response({"error": "Could not import movie"}, status=500)

        return Response({
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "genres": movie.genres,
            "overview": movie.overview,
            "poster": movie.poster,
            "tmdb_id": movie.tmdb_id
        })