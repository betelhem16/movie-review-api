from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
