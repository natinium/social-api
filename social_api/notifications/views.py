"""
This module defines the NotificationViewSet for managing user notifications via the API.
"""
from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsNotificationOwner

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user notifications.
    """
    queryset = Notification.objects.all() # The base queryset for notifications (all notifications).
    serializer_class = NotificationSerializer # The serializer class to use for notification objects.
    permission_classes = [permissions.IsAuthenticated, IsNotificationOwner] # Permissions required for accessing notifications: must be authenticated and own the notification.

    def get_queryset(self):
        """
        Overrides the default queryset to return only the current user's notifications.

        Returns:
            A queryset containing only the current user's notifications.
        """
        return self.queryset.filter(user=self.request.user) # Filter the queryset to only include notifications belonging to the currently authenticated user.