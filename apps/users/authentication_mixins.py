from rest_framework.authentication import get_authorization_header

from apps.users.authentication import ExpiringTokenAuthentication
from rest_framework import exceptions, status, authentication
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class Authentication(authentication.BaseAuthentication):
    user = None

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                msg = 'Invalid token header. Token string should not contain spaces.'
                return None
            
            
            token_expired = ExpiringTokenAuthentication()
            user = token_expired.authenticate_credentials(token)

            if user != None:
                self.user = user
                return user
        return None
    
    def authenticate(self, request):
        self.get_user(request)
        if self.user is None:            
            raise exceptions.AuthenticationFailed('Credentials have not been sent')
        
        return (self.get_user(request), None)
    

    # def dispatch(self, request, *args, **kwargs):
    #     user = self.get_user(request)

    #     if user is not None:
    #             return super().dispatch(request, *args, **kwargs)

    #     response = Response({'error': 'Credentials have not been sent'}, status=status.HTTP_400_BAD_REQUEST)
    #     response.accepted_renderer = JSONRenderer()
    #     response.accepted_media_type = 'application/json'
    #     response.renderer_context = {}

    #     return response