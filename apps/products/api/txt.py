from rest_framework import status
from rest_framework import viewsets
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, UserListSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.all().values('id','username','email','password')
        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message":"User created successfully!"}, status=status.HTTP_201_CREATED)
                             
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):

    user = User.objects.filter(id=pk).first()

    if user:
        if request.method == 'GET':            
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':            
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            username = user.username
            user.delete()
            return Response({'message': f'User {username} deleted'}, status=status.HTTP_200_OK)
        
    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
