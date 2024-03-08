from rest_framework_simplejwt.authentication import JWTAuthentication
from typing import Optional, Tuple
from django.http import HttpRequest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import UntypedToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: HttpRequest) -> Optional[Tuple[User, UntypedToken]]:
        access_token: str = str(request.COOKIES.get('access_token'))
        if access_token:
                token:UntypedToken = self.get_validated_token(access_token)
                user:User = self.get_user(token)
                return user, token
        else:   return None