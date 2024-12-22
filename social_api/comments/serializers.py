"""
This module defines the CommentSerializer for serializing and deserializing Comment objects.
"""
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    user = serializers.ReadOnlyField(source='user.username') # Serializes the username of the user who created the comment. This field is read-only.


    class Meta:
        """
        Meta class for the CommentSerializer.
        """
        model = Comment # Specifies the model to be serialized.
        fields = ['id', 'post', 'user', 'text', 'created_at'] # Specifies the fields to be included in the serialized representation.
