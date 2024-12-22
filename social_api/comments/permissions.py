"""
This module defines a custom permission class for comment ownership.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCommentOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a comment to edit or delete it.
    Read-only access is granted to all users.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the given object (Comment).

        Args:
            request: The incoming request object.
            view: The view handling the request.
            obj: The Comment object being accessed.

        Returns:
            True if the user has permission, False otherwise.
        """
        if request.method in SAFE_METHODS: # Check if the request method is one of the safe methods (GET, HEAD, OPTIONS).
            return True # Allow read access to all users.
        return obj.user == request.user # Only allow the owner of the comment to perform unsafe methods (POST, PUT, DELETE).