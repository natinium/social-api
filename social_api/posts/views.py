"""
This module defines the PostViewSet for managing posts and likes using Django REST Framework.
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing posts and likes.
    Provides CRUD operations for posts and like/unlike actions.
    """
    queryset = Post.objects.all() # Retrieves all Post objects from the database.
    serializer_class = PostSerializer # Specifies the serializer class to use for Post objects.
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] # Sets the permission classes for this viewset.

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method to set the author of the post to the current user.

        Args:
            serializer: The serializer instance.
        """
        serializer.save(author=self.request.user) # Saves the Post object, setting the author to the currently authenticated user.

    @action(detail=True, methods=['post'], permission_classes=[IsAuthorOrReadOnly])
    def like(self, request, pk=None):
        """
        Allows a user to like a post.

        Args:
            request: The request object.
            pk: The primary key of the post to like.

        Returns:
            A Response object with a 'liked' status or an error message.
        """
        post = self.get_object() # Retrieves the Post object based on the provided pk.
        Like.objects.get_or_create(user=request.user, post=post) # Creates a Like object if one doesn't exist, otherwise retrieves the existing one. Prevents duplicate likes.
        return Response({'status': 'liked'}, status=status.HTTP_200_OK) # Returns a successful response with a 'liked' status.

    @action(detail=True, methods=['post'], permission_classes=[IsAuthorOrReadOnly])
    def unlike(self, request, pk=None):
        """
        Allows a user to unlike a post.

        Args:
            request: The request object.
            pk: The primary key of the post to unlike.

        Returns:
            A Response object with an 'unliked' status or an error message.
        """
        post = self.get_object() # Retrieves the Post object based on the provided pk.
        Like.objects.filter(user=request.user, post=post).delete() # Deletes the Like object associated with the user and post.
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK) # Returns a successful response with an 'unliked' status.