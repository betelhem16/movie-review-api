from django.contrib import admin
from django.urls import path, include
from reviews.views import home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('api/users/', include('users.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/movies/', include('movies.urls')),
]
