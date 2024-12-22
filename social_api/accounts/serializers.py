"""
This module defines serializers for the User model.

Includes serializers for:
    - User: Serializes basic user information.
    - Registration: Handles user registration with password validation.
    - Login: Handles user login with email and password.
"""

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes basic user information (id, email, username).
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user registration with password validation.
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Validates that the provided passwords match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Creates a new user instance.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Handles user login with email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
