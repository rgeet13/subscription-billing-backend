from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token["email"] = user.email
        token["is_active"] = user.is_active
        return token

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer