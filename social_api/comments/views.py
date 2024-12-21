from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwnerOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)