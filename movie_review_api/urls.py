from django.contrib import admin
from django.urls import path, include
from reviews.views import home_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('api/users/', include('users.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/movies/', include('movies.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
