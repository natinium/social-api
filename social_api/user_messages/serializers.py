"""
This module defines the MessageSerializer for serializing and deserializing UserMessage objects.
"""
from rest_framework import serializers
from .models import UserMessage

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserMessage model.
    """
    sender = serializers.ReadOnlyField(source='sender.username')  # Serializes the username of the message sender. This field is read-only.

    class Meta:
        """
        Meta class for the MessageSerializer. Defines metadata about the serializer.
        """
        model = UserMessage  # Specifies the model to be serialized (the UserMessage model).
        fields = ['id', 'sender', 'recipient', 'content', 'created_at']  # Specifies the fields to be included in the serialized representation of a UserMessage object.