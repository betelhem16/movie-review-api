# 🎬 Movie Review API

A fully functional RESTful API built with Django and Django REST Framework that allows users to register, log in, and manage movie reviews. It integrates with TMDb to fetch movie data and supports features like JWT authentication, filtering, pagination, and review likes.

---

## 🚀 Project Overview

This API was developed as part of the **ALX Backend Capstone Project**. It mimics a real-world backend service where users can:

- Register and authenticate
- Submit, update, and delete reviews
- View reviews by movie title
- Like reviews
- Discover and import movies from TMDb
- Get movie recommendations

---

## 🧩 Features

- ✅ User registration and JWT authentication
- ✅ Review CRUD with rating validation
- ✅ Like/unlike reviews
- ✅ TMDb movie import, discovery, and recommendations
- ✅ Search, filter, sort, and paginate reviews
- ✅ Permissions: users can only modify their own reviews
- ✅ Ready for deployment on Render or Heroku

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Auth:** JWT via `djangorestframework-simplejwt`
- **External API:** TMDb (The Movie Database)
- **Database:** SQLite (local)


---

Authentication Endpoints
|  |  |  | 
|  | /api/users/register/ |  | 
|  | /api/users/login/ |  | 
|  | /api/users/token/refresh/ |  | 
|  | /api/users/me/ |  | 
|  | /api/users/list/ |  | 



Review Endpoints
|  |  |  | 
|  | /api/reviews/ |  | 
|  | /api/reviews/<id>/ |  | 
|  | /api/reviews/<id>/like/ |  | 




|  |  |  | 
|  | /api/movies/ |  | 
|  | /api/movies/import/ |  | 
|  | /api/movies/discover/ |  | 
|  | /api/movies/popular/ |  | 
|  | /api/movies/<tmdb_id>/recommendations/ |  | 







## 📦 Installation & Setup

### 1. Clone the Repository


git clone https://github.com/betelhem16/movie-review-api.git
cd movie-review-api
# Movie Review API (ALX Capstone) - TMDb Edition

This is a Django + DRF API for movie reviews with TMDb integration.

See docs/dbdiagram.txt for ERD. Use .env.example to set TMDB_API_KEY.

Local setup:
1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. cp .env.example .env and set keys
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver


