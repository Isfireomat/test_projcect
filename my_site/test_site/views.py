from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse,HttpResponseRedirect,redirect
from django.http import HttpRequest, HttpResponse
from rest_framework import permissions, views
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Union
from .serializers import *
from .authentication import CustomJWTAuthentication

class index(views.APIView):
    def get(self,request:HttpRequest)-> HttpResponseRedirect:
        return redirect('register')

class RegisterView(views.APIView):
    permission_classes:list = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def get(self,request:HttpRequest)-> HttpResponse: return render(request,'temp1/reg.html')

    def post(self,request:HttpRequest)->HttpResponseRedirect:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponseRedirect('/login/')



class LoginView(views.APIView):
    permission_classes=[permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def get(self,request:HttpRequest)-> HttpResponse: return render(request,'temp1/login.html')
    
    def post(self,request:HttpRequest):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:User = serializer.validated_data
        request.session['name'] = user.username
        request.session['email'] = user.email

        refresh_token:RefreshToken=RefreshToken.for_user(user)
        access_token:str=str(refresh_token.access_token)
        
        response:HttpResponseRedirect=HttpResponseRedirect('/account/')
        response.set_cookie('access_token', access_token,httponly=True)
        response.set_cookie('refresh_token', str(refresh_token),httponly=True)
        
        return response



class AccountView(views.APIView):
    authentication_classes:list = [CustomJWTAuthentication]
    permission_classes:list = [permissions.IsAuthenticated]
    
    def get(self, request:HttpRequest)-> HttpResponse:
        user:User = request.user
        name:str = user.username
        email:str = user.email
        return render(request, 'temp1/user_acc.html', {"name": name, "email": email})
    
    def post(self,request:HttpRequest)->Union[HttpResponseRedirect, HttpResponse]:
        if request.data['logout']:
            refresh_token:str = request.COOKIES.get('refresh_token')
            if refresh_token:
                try:
                    token:RefreshToken = RefreshToken(refresh_token)
                    token.blacklist()
                    response:HttpResponseRedirect = HttpResponseRedirect('/login/')
                    response.delete_cookie('refresh_token')
                    response.delete_cookie('access_token')
                    return response
                except Exception as e:
                    return render(request, 'temp1/error.html', {"error_message": str(e)})
            else:
                return render(request, 'temp1/error.html', {"error_message": "refresh token is not exist"})  