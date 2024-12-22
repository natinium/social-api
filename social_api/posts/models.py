"""
This module defines the Post and Like models for a simple blogging application.
"""
from django.db import models
from django.conf import settings

class Post(models.Model):
    """
    Represents a blog post.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # The author of the post. If the author is deleted, the post is also deleted.
    title = models.CharField(max_length=200) # The title of the post.
    content = models.TextField() # The content of the post.
    created_at = models.DateTimeField(auto_now_add=True) # The timestamp when the post was created. Automatically set on creation.

class Like(models.Model):
    """
    Represents a like on a post by a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # The user who liked the post. If the user is deleted, the like is also deleted.
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # The post that was liked. If the post is deleted, the like is also deleted.
    created_at = models.DateTimeField(auto_now_add=True) # The timestamp when the like was created. Automatically set on creation.

    class Meta:
        """
        Meta class for the Like model. Defines metadata about the model.
        """
        unique_together = ('user', 'post') # Ensures that a user can only like a post once.