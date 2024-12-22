"""
This module contains API tests for the Comment model.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from posts.models import Post
from rest_framework.authtoken.models import Token
from .models import Comment

class CommentAPITest(APITestCase):
    """
    API test class for testing Comment creation.
    """
    def setUp(self):
        """
        Set up method to create a test user, token, and post before each test.
        """
        self.user = User.objects.create_user(email='test@test.com', username='testuser',password='testpass123') # Create a test user.
        self.token = Token.objects.create(user=self.user) # Create a token for the test user.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # Authenticate the client with the token.
        self.post = Post.objects.create(author=self.user,title='Post',content='Content') # Create a test post associated with the test user.

    def test_create_comment(self):
        """
        Test that an authenticated user can successfully create a comment.
        """
        url = reverse('comment-list') # Get the URL for the comment list endpoint.
        data = {'post': self.post.id, 'text': 'Nice post'} # Create the data for the comment.
        response = self.client.post(url, data) # Make a POST request to create the comment.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Assert that the response status code is 201 Created.
        self.assertTrue(Comment.objects.filter(post=self.post, user=self.user).exists()) # Assert that the comment was actually created in the database.