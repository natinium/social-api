"""
This module defines the Comment model.
"""
from django.db import models
from django.conf import settings
from posts.models import Post

class Comment(models.Model):
    """
    Represents a comment on a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # Foreign key to the Post model. When a post is deleted, all associated comments are also deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Foreign key to the User model (defined in settings). When a user is deleted, their comments are also deleted.
    text = models.TextField() # The text content of the comment.
    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the creation timestamp when the comment is created.