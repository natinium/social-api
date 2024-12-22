"""
This module defines the CommentViewSet for managing comments using Django REST framework.
"""
from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwnerOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing comments on posts.
    """
    queryset = Comment.objects.all() # All comments are retrieved by default.
    serializer_class = CommentSerializer # CommentSerializer is used for serialization and deserialization.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]  # Permissions for accessing and modifying comments.

    def perform_create(self, serializer):
        """
        Overrides the default behavior to save the comment with the logged-in user as the author.

        Args:
            serializer: The CommentSerializer instance containing validated comment data.
        """
        serializer.save(user=self.request.user)  # Save the comment with the request user.