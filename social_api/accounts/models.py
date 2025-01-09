"""
This module defines custom user and follow models for a Django application.

The `User` model extends Django's `AbstractUser` and uses email as the unique identifier.
It also requires the username field during user creation.

The `Follow` model represents the relationship between two users where one user
follows another. It includes fields for the follower, the followed user,
and the timestamp of the follow action.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model that uses email as the unique identifier.
    """
    email = models.EmailField(unique=True)

    # Set email as the unique identifier for user authentication
    USERNAME_FIELD = 'email'
    # Require username field during user creation
    REQUIRED_FIELDS = ['username']


class Follow(models.Model):
    """
    Model to represent a user following another user.
    """
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    """
    ForeignKey to the User model representing the user who is following.
    related_name: Allows accessing the users this user is following.
    on_delete: CASCADE deletes the follow relationship if the followed user is deleted.
    """
    following = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE
    )
    """
    ForeignKey to the User model representing the user being followed.
    related_name: Allows accessing the users who follow this user.
    on_delete: CASCADE deletes the follow relationship if the followed user is deleted.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """
    DateTimeField that automatically records the creation time of the follow relationship.
    """

    class Meta:
        """
        Meta class to define model-level options.
        """
        unique_together = ('follower', 'following')
        """
        Ensures that a user can only follow another user once.
        """