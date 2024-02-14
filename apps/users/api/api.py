from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data)
    
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)
    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    user = User.objects.filter(id=pk).first()
    if user:
        if request.method == 'GET':            
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
        
        if request.method == 'PUT':            
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data)
            return Response(user_serializer.errors)
        
        if request.method == 'DELETE':
            username = user.username
            user.delete()
            return Response({'message': f'User {username} deleted'}, status=200)
        
    return Response({'message': 'User not found'}, status=400)
