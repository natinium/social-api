"""
This module defines the MessageViewSet for managing user messages using Django REST framework.
"""
from rest_framework import viewsets, permissions
from .models import UserMessage
from .serializers import MessageSerializer
from .permissions import IsSenderOrRecipient

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user messages (CRUD operations).
    """

    queryset = UserMessage.objects.all()  # Retrieves all UserMessage objects from the database.
    serializer_class = MessageSerializer  # Serializer class used for serializing and deserializing UserMessage objects.
    permission_classes = [permissions.IsAuthenticated, IsSenderOrRecipient]  # Permissions required for accessing messages.

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method to set the sender of the message to the currently authenticated user.

        Args:
            serializer: The serializer instance containing the message data.
        """
        serializer.save(sender=self.request.user)  # Saves the message, setting the sender to the authenticated user.