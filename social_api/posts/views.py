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
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Override the default perform_create method to set the author of the post
        to the current user.
        """
        serializer.save(author=self.request.user)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthorOrReadOnly])
    def like(self, request, pk=None):
        """
        Allows a user to like a post.
        """
        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthorOrReadOnly])
    def unlike(self, request, pk=None):
        """
        Allows a user to unlike a post.
        """
        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)