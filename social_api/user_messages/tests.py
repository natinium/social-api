from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from rest_framework.authtoken.models import Token
from .models import UserMessage

class MessageAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123')
        self.user2 = User.objects.create_user(email='other@test.com',username='otheruser',password='pass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_send_message(self):
        url = reverse('message-list')
        data = {'recipient': self.user2.id, 'content': 'Hello'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserMessage.objects.filter(sender=self.user, recipient=self.user2).exists())