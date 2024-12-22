"""
This module defines the UserMessage model for storing messages between users.
"""
from django.db import models
from django.conf import settings

class UserMessage(models.Model):
    """
    Represents a message sent from one user to another.
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE) # The user who sent the message. If the sender is deleted, the message is also deleted. The related_name allows easy access to messages sent by a user (e.g., user.sent_messages.all()).
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE) # The user who received the message. If the recipient is deleted, the message is also deleted. The related_name allows easy access to messages received by a user (e.g., user.received_messages.all()).
    content = models.TextField() # The text content of the message.
    created_at = models.DateTimeField(auto_now_add=True) # The timestamp when the message was created. Automatically set on creation.