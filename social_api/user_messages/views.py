from rest_framework import viewsets, permissions
from .models import UserMessage
from .serializers import MessageSerializer
from .permissions import IsSenderOrRecipient

class MessageViewSet(viewsets.ModelViewSet):
    queryset = UserMessage.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrRecipient]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)