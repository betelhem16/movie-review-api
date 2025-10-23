import os
import requests
from django.shortcuts import render
from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review, Movie, Like
from .serializers import ReviewSerializer, MovieSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from movies.tmdb import get_or_create_movie_by_title  # implement in movies/tmdb.py



class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'movie__title']
    search_fields = ['movie_title', 'review_text']
    ordering_fields = ['rating', 'created_at']

    def perform_create(self, serializer):
        title = serializer.validated_data.get('movie_title')
        movie = get_or_create_movie_by_title(title)
        serializer.save(owner=self.request.user, movie=movie)

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, review=review)
        if not created:
            # toggle off
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)
        return Response({"liked": True}, status=status.HTTP_201_CREATED)
    
def home_view(request):
    """
    Simple home page for the Movie Review API.
    """
    return render(request, "reviews/index.html", context={
        "project_name": "Movie Review API",
    })