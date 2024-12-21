from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsNotificationOwner

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotificationOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)