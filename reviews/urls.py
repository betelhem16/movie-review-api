from django.urls import path
from .views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView, LikeToggleView
urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='reviews_list_create'),
    path('<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review_detail'),
    path('<int:pk>/like/', LikeToggleView.as_view(), name='reviews-like'),
]
