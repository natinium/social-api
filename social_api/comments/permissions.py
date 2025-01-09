"""
This module defines a custom permission class for comment ownership.
"""
from rest_framework import permissions

class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow the comment owner to edit/delete the comment.
    Otherwise, read-only.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user