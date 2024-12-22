"""
This module defines a custom permission class to check if a user is either the sender or recipient of a message.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSenderOrRecipient(BasePermission):
    """
    Custom permission to allow only the sender or recipient of a message to access it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user making the request is either the sender or the recipient of the message.

        Args:
            request: The request object.
            view: The view handling the request.
            obj: The UserMessage object being accessed.

        Returns:
            True if the user is either the sender or the recipient, False otherwise.
        """
        return obj.sender == request.user or obj.recipient == request.user  # Returns True if the requesting user is either the sender or recipient of the message.