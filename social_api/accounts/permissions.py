"""
This module defines a custom permission class to check if the user is authenticated.
"""

from rest_framework.permissions import BasePermission

class IsAuthenticatedUser(BasePermission):
    """
    Checks if the user is authenticated.
    """
    def has_permission(self, request, view):
        """
        Returns True if the user is authenticated, False otherwise.
        """
        return request.user and request.user.is_authenticated
