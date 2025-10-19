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

Pushing to GitHub & deploying to PythonAnywhere or Heroku are described in the full README above in the earlier message.
