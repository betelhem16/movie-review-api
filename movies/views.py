

# Create your views here.
# movies/views.py
from rest_framework import generics, filters
from .models import Movie
from .serializers import MovieSerializer

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

        with_genres = None
        if genre_name:
            mapping = get_genre_mapping()
            with_genres = mapping.get(genre_name.lower())

        data = discover_movies(page=page, sort_by=sort_by, with_genres=with_genres, region=region, with_original_language=original_lang)
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']