"""
This module defines the Notification model for storing user notifications.
"""
from django.db import models
from django.conf import settings

class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications') # The user to whom the notification belongs. When a user is deleted, their notifications are also deleted.
    message = models.CharField(max_length=255) # The notification message.
    created_at = models.DateTimeField(auto_now_add=True) # The timestamp when the notification was created. Automatically set on creation.
    read = models.BooleanField(default=False) # Indicates whether the notification has been read by the user. Defaults to False.