from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.api.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer

from apps.users.models import User

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username','')
        password = request.data.get('password','')

        user = authenticate(username=username, password=password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'user': user_serializer.data,
                    'token': login_serializer.validated_data.get("access"),
                    'refresh-token': login_serializer.validated_data.get("refresh"),
                    'message': 'User logged in successfully'
                }, status = status.HTTP_200_OK)
            
            return Response({"error":"Invalid username or password"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response({"error":"Invalid username or password"}, status = status.HTTP_401_UNAUTHORIZED)


class Logout(GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get("user",""))

        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({"message":"User logged out successfully"}, status = status.HTTP_200_OK)
        
        return Response({"error":"User not found"}, status = status.HTTP_404_NOT_FOUND)
