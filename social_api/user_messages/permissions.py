from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSenderOrRecipient(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.recipient == request.user