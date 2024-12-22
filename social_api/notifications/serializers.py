"""
This module defines the NotificationSerializer for serializing and deserializing Notification objects.
"""
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    """
    class Meta:
        """
        Meta class for the NotificationSerializer. Defines metadata about the serializer.
        """
        model = Notification  # Specifies the model to be serialized.
        fields = ['id', 'user', 'message', 'read', 'created_at']  # Specifies the fields to be included in the serialized output.