"""
This module defines the CommentViewSet for managing comments using Django REST framework.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwnerOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing comments on posts.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Save the comment with the logged-in user as the author.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='post/(?P<post_id>[^/.]+)/list')
    def get_comments_by_post(self, request, post_id=None):
        """
        Custom endpoint to get a list of comments for a single post by its ID.
        e.g. GET /comments/post/1/list/
        """
        comments = Comment.objects.filter(post_id=post_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)