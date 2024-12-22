"""
This module defines a custom permission class to check notification ownership.
"""
from rest_framework.permissions import BasePermission

class IsNotificationOwner(BasePermission):
    """
    Custom permission to only allow the owner of a notification to access it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user making the request is the owner of the notification.

        Args:
            request: The request object.
            view: The view handling the request.
            obj: The Notification object being accessed.

        Returns:
            True if the user is the owner, False otherwise.
        """
        return obj.user == request.user # Check if the notification's user is the same as the requesting user.