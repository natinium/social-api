from rest_framework import serializers
from .models import UserMessage

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    class Meta:
        model = UserMessage
        fields = ['id', 'sender', 'recipient', 'content', 'created_at']