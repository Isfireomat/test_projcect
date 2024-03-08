from rest_framework_simplejwt.tokens import RefreshToken,UntypedToken
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest)-> HttpResponse:
        try:
            refresh_token:str = request.COOKIES.get('refresh_token')
            access_token:str = request.COOKIES.get('access_token') 
            if access_token and UntypedToken(access_token,verify=False).payload['exp'] < datetime.utcnow().timestamp() and refresh_token :
                try:
                    refreshed_token: RefreshToken = RefreshToken(refresh_token)
                    access_token:str= str(refreshed_token.access_token)
                    request.COOKIES['access_token'] = access_token
                except Exception as e:
                    return render(request, 'temp1/error.html', {"error_message": "Error with refresh token"}) 
        except:...    
        response: HttpResponse = self.get_response(request)
        if access_token:response.set_cookie('access_token', access_token)
        return response