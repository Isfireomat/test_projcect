from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from typing import Any, Dict

class RegisterSerializer(serializers.ModelSerializer):
    password:serializers.CharField = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data: Dict[str, Any]) -> User:
        user:User = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username:serializers.CharField = serializers.CharField(max_length=255)
    password:serializers.CharField = serializers.CharField(max_length=255)
    
    def validate(self, data: Dict[str, str]) -> User:
        username: str = data['username']
        password: str  = data['password']
        user: User = authenticate(username=username, password=password)
        if not user: raise AuthenticationFailed('Incorrect username or password.')
        return user
    
class UserSerializer(serializers.Serializer):
    id:serializers.IntegerField = serializers.IntegerField(source='pk')
    username:serializers.CharField = serializers.CharField()
    email:serializers.EmailField = serializers.EmailField()