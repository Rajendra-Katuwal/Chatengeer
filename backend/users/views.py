from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import MyTokenObtainPairSerializer



User = get_user_model()

class RegisterView( generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
