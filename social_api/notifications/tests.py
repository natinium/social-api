from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from rest_framework.authtoken.models import Token
from .models import Notification

class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.notification = Notification.objects.create(user=self.user, message='You got a like')

    def test_list_notifications(self):
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)