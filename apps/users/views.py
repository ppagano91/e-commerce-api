from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import UserTokenSerializer

class UserToken(Authentication, APIView):
    def get(self, request):        
        try:
            username = UserTokenSerializer.Meta.model.objects.filter(username=self.user.username).first()
            user_token, _ = Token.objects.get_or_create(user = username)

            if user_token:
                user = user_token.user
                token = user_token.key
                user_serializer = UserTokenSerializer(user)
                return Response({"token": token, "user":user_serializer}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Token not found in the request"}, status=status.HTTP_404_NOT_FOUND)

class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request': request})        
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']

            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)

                if created:
                    return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Token created successfuly!'}, status=status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    
                    if all_sessions.exists():
                        if all_sessions.count() > 1:
                            for session in all_sessions:
                                session_data = session.get_decoded()
                                if user.id == int(session_data.get('_auth_user_id')):
                                    session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Token created successfuly!'}, status=status.HTTP_201_CREATED)
                    # return Response({"error": "This user already has an associated token"}, status=status.HTTP_409_CONFLICT)                
            else:
                return Response({'error': 'This user is not active'}, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    
    def get(self, request):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                session_message = None
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                            session_message = "User sessions deleted"

                token.delete()
                token_message = "Token deleted"

                return Response({"token_message": token_message, "session_message": session_message}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Token not found in the request"}, status=status.HTTP_404_NOT_FOUND)