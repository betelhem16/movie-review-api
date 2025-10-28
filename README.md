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
## 🔐 Authentication Endpoints

| Method         | Endpoint                          | Description                            |
|----------------|-----------------------------------|----------------------------------------|
| POST           | `/api/users/register/`            | Register a new user                    |
| POST           | `/api/users/login/`               | Obtain JWT token                       |
| POST           | `/api/users/token/refresh/`       | Refresh JWT token                      |
| GET / PUT / DELETE | `/api/users/me/`              | View, update, or delete current user   |
| GET            | `/api/users/list/`                | List all users                         |

---

## 📝 Review Endpoints

| Method         | Endpoint                          | Description                            |
|----------------|-----------------------------------|----------------------------------------|
| GET / POST     | `/api/reviews/`                   | List all reviews or create a new one   |
| GET / PUT / DELETE | `/api/reviews/<id>/`          | Retrieve, update, or delete a review   |
| POST           | `/api/reviews/<id>/like/`         | Like or unlike a review                |

---

## 🎬 Movie Endpoints

| Method         | Endpoint                                          | Description                                      |
|----------------|---------------------------------------------------|--------------------------------------------------|
| GET            | `/api/movies/`                                    | List movies                                      |
| POST           | `/api/movies/import/`                             | Import movie by TMDb ID                          |
| GET            | `/api/movies/discover/`                           | Discover trending or genre-based movies         |
| GET            | `/api/movies/popular/`                            | View popular movies                              |
| GET            | `/api/movies/<tmdb_id>/recommendations/`          | Get recommended movies based on TMDb ID         |

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


