from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.api.serializers import UserTokenSerializer

class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request': request})        
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']

            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                print("user\n", user)
                user_serializer = UserTokenSerializer(user)

                if created:
                    return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Token created successfuly!'}, status=status.HTTP_201_CREATED)
                else:
                    '''
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    
                    if all_sessions.exists():
                        if all_sessions.count() > 1:
                            for session in all_sessions:
                                session_data = session.get_decoded()
                                if user.id == int(session_data.get('_auth_user_id')):
                                    session.delete()
                    #    else:
                    #       session_data = all_sessions.first().get_decoded()
                    #       if user.id == int(session_data.get('_auth_user_id')):
                    #           all_sessions.first().delete()
                    
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Token created successfuly!'}, status=status.HTTP_201_CREATED)
                    '''
                    token.delete()
                    return Response({"error": "This user already has an associated token"}, status=status.HTTP_409_CONFLICT)

                return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Successful login!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'This user is not active'}, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
