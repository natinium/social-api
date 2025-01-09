"""
This module defines the API endpoints for user management, including registration,
login, following/unfollowing, using Django REST Framework.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User, Follow
from .serializers import (
    UserSerializer,
    RegistrationSerializer,
    LoginSerializer
)
from .permissions import IsAuthenticatedUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users, including registration, login, follow/unfollow actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'register': [AllowAny],
        'login': [AllowAny],
        'default': [IsAuthenticated, IsAuthenticatedUser]
    }

    def get_permissions(self):
        """
        Return the permission classes depending on the current action.
        """
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]

    def get_serializer_class(self):
        """
        Determines the appropriate serializer class based on the action being performed.
        """
        if self.action == 'register':
            return RegistrationSerializer
        elif self.action == 'login':
            return LoginSerializer
        return UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Logs in a user and returns an authentication token upon successful credentials.

        **Request:**
            - data: Dictionary containing email and password fields.

        **Response:**
            - On success:
                - token: Authentication token for the user.
                - user_id: User ID of the logged-in user.
                - email: Email address of the user.
                - username: Username of the user.
            - On failure (400 Bad Request):
                - error: Description of the error (e.g., Invalid credentials).
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Registers a new user and returns an authentication token upon successful registration.

        **Request:**
            - data: Dictionary containing user information according to the RegistrationSerializer.

        **Response:**
            - On success (201 Created):
                - token: Authentication token for the newly registered user.
                - user_id: User ID of the newly registered user.
                - email: Email address of the user.
                - username: Username of the user.
            - On failure (400 Bad Request):
                - Details of the validation errors encountered during registration.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """
        Allows a logged-in user to follow another user.

        **Request:** (Requires authentication and valid user permissions)

        **Response:**
            - On success (200 OK):
                - status: 'followed' indicating successful follow action.
            - On failure (400 Bad Request):
                - error: Description of the error (e.g., Cannot follow yourself).
        """
        user_to_follow = self.get_object()
        if request.user == user_to_follow:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        return Response({'status': 'followed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """
        Allows a logged-in user to unfollow another user.

        **Request:** (Requires authentication and valid user permissions)

        **Response:**
            - On success (200 OK):
                - status: 'unfollowed' indicating successful unfollow action.
        """
        user_to_unfollow = self.get_object()
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """
        Retrieves the list of users who follow this user (specified by pk),
        along with the total count of followers.
        """
        user = self.get_object()
        followers_qs = user.followers.all()
        followers_data = [
            {
                'id': follow.follower.id,
                'email': follow.follower.email,
                'username': follow.follower.username
            }
            for follow in followers_qs
        ]
        return Response({
            'count': followers_qs.count(),
            'followers': followers_data
        }, status=status.HTTP_200_OK)