from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, UserListSerializer, UserUpdateSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
# Difference between GenericViewSet and ModelViewSet:
# 
# GenericViewSet: It is used when you don't need to perform CRUD operations on a model. It is used when you need to perform custom operations on a model.
# ModelViewSet: It is used when you need to perform CRUD operations on a model. It is used when you need to perform operations like create, retrieve, update, and delete on a model.
class UserViewSet(viewsets.GenericViewSet):
    model = User
    list_serializer_class = UserListSerializer
    serializer_class = UserSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(is_active=True).values('id','name','username','email', 'password')
        return self.queryset
    
    def list(self, request):        
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message":"User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        user = self.get_object(pk)        
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def update (self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UserUpdateSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message":"User updated successfully!"}, status=status.HTTP_200_OK)
        return Response({
            "message":"User not found",
            "error":user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user = self.model.objects.filter(id=pk)
        user_destroy = user.update(is_active=False)
        if user_destroy == 1:
            username = user.first().username
            return Response({'message': f'User {username} deleted'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)