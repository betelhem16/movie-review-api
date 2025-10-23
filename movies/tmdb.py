# movies/tmdb.py
import os
import requests
from django.core.cache import cache
from django.conf import settings
from reviews.models import Movie

# --- CONFIG ---
TMDB_API_KEY = os.getenv('TMDB_API_KEY') or getattr(settings, 'TMDB_API_KEY', None)
BASE = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


# --- HELPER FUNCTION TO CALL TMDB ---
def tmdb_get(path, params=None, cache_key=None, cache_timeout=60 * 30):
    """Handles requests to TMDB API safely with caching."""
    if not TMDB_API_KEY:
        print("⚠️ Missing TMDB_API_KEY. Please set it in your .env or settings.py")
        return None

    if params is None:
        params = {}
    params['api_key'] = TMDB_API_KEY
    url = f"{BASE}{path}"

    if cache_key:
        data = cache.get(cache_key)
        if data is not None:
            return data

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if cache_key:
            cache.set(cache_key, data, cache_timeout)
        return data
    except requests.exceptions.RequestException as e:
        print(f"TMDB request error: {e}")
        return None


# --- SEARCH MOVIE BY TITLE ---
def search_movie(title):
    if not title:
        return None
    return tmdb_get("/search/movie", {"query": title, "include_adult": False}, cache_key=f"tmdb_search_{title}")


# --- GET DETAILS FOR A SPECIFIC MOVIE ---
def get_movie_details(tmdb_id):
    if not tmdb_id:
        return None
    return tmdb_get(f"/movie/{tmdb_id}", cache_key=f"tmdb_movie_{tmdb_id}")


# --- IMAGE HANDLER ---
def poster_url(path):
    if not path:
        return None
    return f"{IMAGE_BASE}{path}"

# --- GENRES LIST FROM TMDB ---
def get_genre_mapping():
    """Returns a dictionary of TMDB genre id -> name."""
    data = tmdb_get("/genre/movie/list", cache_key="tmdb_genres")
    if not data or "genres" not in data:
        return {}
    return {genre["id"]: genre["name"] for genre in data["genres"]}


# --- DISCOVER MOVIES (POPULAR / TOP RATED ETC.) ---
def discover_movies(sort_by="popularity.desc", genre_id=None, page=1):
    """Fetches a list of movies from TMDB's discover endpoint."""
    params = {"sort_by": sort_by, "page": page}
    if genre_id:
        params["with_genres"] = genre_id
    return tmdb_get("/discover/movie", params=params, cache_key=f"tmdb_discover_{sort_by}_{genre_id}_{page}")

# --- CORE FUNCTION USED IN YOUR VIEWS ---
def get_or_create_movie_by_title(title):
    """Returns a Movie instance for a given title (fetching from TMDB if not in DB)."""
    if not title:
        title = "Unknown Movie"

    # 1. Check local DB first
    existing = Movie.objects.filter(title__iexact=title).first()
    if existing:
        return existing

    # 2. Search from TMDB
    search = search_movie(title)
    if search and "results" in search and search["results"]:
        top = search["results"][0]
        tmdb_id = top.get("id")
        details = get_movie_details(tmdb_id) or top

        movie, _ = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "title": details.get("title") or title,
                "year": (details.get("release_date") or "")[:4],
                "overview": details.get("overview") or "",
                "poster": poster_url(details.get("poster_path")),
            },
        )

        # Save genres if available
        genres = ", ".join([g['name'] for g in details.get('genres', [])]) if details.get("genres") else ""
        if genres:
            movie.genres = genres
            movie.save()

        return movie

    # 3. Fallback: create minimal movie if TMDB fails
    return Movie.objects.create(title=title)
