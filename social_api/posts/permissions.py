"""
This module defines a custom permission class for checking post ownership.
"""
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow authors of posts to edit or delete them,
    and allow read-only access to all users.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the given object (Post).

        Args:
            request: The request object.
            view: The view handling the request.
            obj: The Post object being accessed.

        Returns:
            True if the user has permission, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            # Read-only methods (GET, HEAD, OPTIONS) are allowed to all users.
            return True
        # For non-safe methods (PUT, PATCH, DELETE), check if the user is the author of the post.
        return obj.author == request.user