# movies/tmdb.py
import os
import requests
from django.core.cache import cache
from django.conf import settings

TMDB_API_KEY = os.getenv('TMDB_API_KEY') or getattr(settings, 'TMDB_API_KEY', None)
BASE = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

def tmdb_get(path, params=None, cache_key=None, cache_timeout=60*60):
    if params is None:
        params = {}
    params['api_key'] = TMDB_API_KEY
    url = f"{BASE}{path}"
    if cache_key:
        data = cache.get(cache_key)
        if data is not None:
            return data
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        if cache_key:
            cache.set(cache_key, data, cache_timeout)
        return data
    except requests.RequestException:
        return None

def search_movie(title, page=1):
    return tmdb_get("/search/movie", {"query": title, "page": page, "include_adult": False},
                    cache_key=f"tmdb_search_{title}_{page}", cache_timeout=60*60)

def get_movie_details(tmdb_id):
    return tmdb_get(f"/movie/{tmdb_id}", cache_key=f"tmdb_movie_{tmdb_id}", cache_timeout=60*60*6)

def discover_movies(page=1, sort_by="popularity.desc", with_genres=None, region=None,
                    language="en-US", with_original_language=None, year=None):
    params = {"page": page, "sort_by": sort_by, "language": language, "include_adult": False}
    if with_genres:
        params["with_genres"] = with_genres
    if region:
        params["region"] = region
    if with_original_language:
        params["with_original_language"] = with_original_language
    if year:
        params["primary_release_year"] = year
    cache_key = f"tmdb_discover_{with_genres}_{region}_{sort_by}_{page}_{with_original_language}_{year}"
    return tmdb_get("/discover/movie", params, cache_key=cache_key, cache_timeout=60*30)

def get_genre_mapping():
    cache_key = "tmdb_genre_map"
    mapping = cache.get(cache_key)
    if mapping:
        return mapping
    data = tmdb_get("/genre/movie/list", {"language": "en-US"})
    mapping = {}
    if data and data.get("genres"):
        for g in data["genres"]:
            mapping[g['name'].lower()] = str(g['id'])
    cache.set(cache_key, mapping, 60*60*24)
    return mapping

def poster_url(poster_path):
    if not poster_path:
        return None
    return f"{IMAGE_BASE}{poster_path}"
