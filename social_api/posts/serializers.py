"""
This module defines the PostSerializer for serializing and deserializing Post objects.
"""
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    author = serializers.ReadOnlyField(source='author.username')

    # Added fields to display the total number of likes and the users who liked the post
    likes_count = serializers.SerializerMethodField()
    likers = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'likes_count',
            'likers',
        ]

    def get_likes_count(self, obj):
        """
        Return the total number of likes for this post.
        """
        return obj.like_set.count()

    def get_likers(self, obj):
        """
        Return a list of usernames who liked this post.
        """
        return [like.user.username for like in obj.like_set.all()]