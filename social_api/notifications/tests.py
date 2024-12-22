"""
This module contains API tests for the Notification model.
"""

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from rest_framework.authtoken.models import Token
from .models import Notification


class NotificationAPITest(APITestCase):
    """
    API test class for testing Notification listing.
    """

    def setUp(self):
        """
        Set up method to create a test user, token, and notification before each test.
        """
        self.user = User.objects.create_user(email='test@test.com', username='testuser', password='testpass123')  # Create a test user.
        self.token = Token.objects.create(user=self.user)  # Create a token for the test user.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Authenticate the client with the token.
        self.notification = Notification.objects.create(user=self.user, message='You got a like')  # Create a test notification for the user.

    def test_list_notifications(self):
        """
        Test that an authenticated user can retrieve their list of notifications.
        """
        url = reverse('notification-list')  # Get the URL for the notification list endpoint.
        response = self.client.get(url)  # Make a GET request to retrieve the notification list.
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assert that the response status code is 200 OK.
        self.assertEqual(len(response.data), 1)  # Assert that the response data contains one notification (the one created in setUp).