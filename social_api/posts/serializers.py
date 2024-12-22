"""
This module defines the PostSerializer for serializing and deserializing Post objects.
"""
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    author = serializers.ReadOnlyField(source='author.username')  # Serializes the username of the post's author. This field is read-only.

    class Meta:
        """
        Meta class for the PostSerializer. Defines metadata about the serializer.
        """
        model = Post  # Specifies the model to be serialized (the Post model).
        fields = ['id', 'title', 'content', 'author', 'created_at']  # Specifies the fields to be included in the serialized representation of a Post object.