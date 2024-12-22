"""
This module contains API tests for the UserMessage model.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from rest_framework.authtoken.models import Token
from .models import UserMessage

class MessageAPITest(APITestCase):
    """
    API test class for testing UserMessage sending functionality.
    """

    def setUp(self):
        """
        Set up method to create test users and authenticate a client before each test.
        """
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123') # Creates a test user.
        self.user2 = User.objects.create_user(email='other@test.com',username='otheruser',password='pass') # Creates a second test user (recipient).
        self.token = Token.objects.create(user=self.user) # Creates a token for the first test user.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # Authenticates the test client using the token.

    def test_send_message(self):
        """
        Test that a user can successfully send a message to another user.
        """
        url = reverse('message-list') # Reverses the URL for the message list endpoint.
        data = {'recipient': self.user2.id, 'content': 'Hello'} # Creates the data for the POST request (recipient ID and message content).
        response = self.client.post(url, data) # Sends a POST request to the message list endpoint with the data.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Asserts that the response status code is 201 Created (successful creation).
        self.assertTrue(UserMessage.objects.filter(sender=self.user, recipient=self.user2).exists()) # Asserts that a UserMessage object exists in the database with the correct sender and recipient.