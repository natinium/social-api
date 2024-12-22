"""
This module contains unit and API tests for the Post and Like models.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from .models import Post, Like
from rest_framework.authtoken.models import Token

class PostModelTest(TestCase):
    """
    Unit tests for the Post model.
    """
    def setUp(self):
        """
        Set up method to create a test user and post before each test.
        """
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123') # Creates a test user.
        self.post = Post.objects.create(author=self.user,title='Test Post',content='Test Content') # Creates a test post associated with the user.

    def test_post_creation(self):
        """
        Test that a Post object is created correctly.
        """
        self.assertTrue(isinstance(self.post, Post)) # Checks if the created object is an instance of the Post model.

class PostAPITest(APITestCase):
    """
    API tests for the Post model.
    """
    def setUp(self):
        """
        Set up method to create a test user, token, and post before each test.
        """
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123') # Creates a test user.
        self.token = Token.objects.create(user=self.user) # Creates a token for the test user for authentication.
        self.api_authentication() # Calls the helper method to authenticate the API client.
        self.post = Post.objects.create(author=self.user,title='Test Post',content='Test Content') # Creates a test post associated with the user.

    def api_authentication(self):
        """
        Helper method to authenticate the API client with the user's token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}') # Sets the Authorization header with the user's token.

    def test_post_list(self):
        """
        Test retrieving a list of posts.
        """
        url = reverse('post-list') # Gets the URL for the post list endpoint.
        response = self.client.get(url) # Makes a GET request to the post list endpoint.
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Asserts that the response status code is 200 OK.
        self.assertEqual(len(response.data), 1) # Asserts that the response contains one post (the one created in setUp).

    def test_post_create(self):
        """
        Test creating a new post.
        """
        url = reverse('post-list') # Gets the URL for the post list endpoint.
        data = {'title': 'New Post','content': 'New Content'} # Data for the new post.
        response = self.client.post(url, data) # Makes a POST request to create the post.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Asserts that the response status code is 201 Created.

    def test_post_update(self):
        """
        Test updating an existing post.
        """
        url = reverse('post-detail', kwargs={'pk': self.post.pk}) # Gets the URL for the specific post's detail endpoint.
        data = {'title': 'Updated Post','content': 'Updated Content'} # Data for updating the post.
        response = self.client.put(url, data) # Makes a PUT request to update the post.
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Asserts that the response status code is 200 OK.

    def test_post_delete(self):
        """
        Test deleting an existing post.
        """
        url = reverse('post-detail', kwargs={'pk': self.post.pk}) # Gets the URL for the specific post's detail endpoint.
        response = self.client.delete(url) # Makes a DELETE request to delete the post.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # Asserts that the response status code is 204 No Content.

    def test_unauthorized_post_create(self):
        """
        Test creating a post without authentication (should fail).
        """
        self.client.credentials() # Removes any existing authentication credentials.
        url = reverse('post-list') # Gets the URL for the post list endpoint.
        data = {'title': 'New Post','content': 'New Content'} # Data for the new post.
        response = self.client.post(url, data) # Makes a POST request to create the post.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Asserts that the response status code is 401 Unauthorized.

    def test_unauthorized_post_update(self):
        """
        Test updating a post with a different user's token (should be forbidden).
        """
        other_user = User.objects.create_user(email='other@test.com',username='otheruser',password='testpass123') # Creates another user.
        other_token = Token.objects.create(user=other_user) # Creates a token for the other user.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}') # Authenticates the client with the other user's token.
        url = reverse('post-detail', kwargs={'pk': self.post.pk}) # Gets the URL for the specific post's detail endpoint.
        data = {'title': 'Updated Post','content': 'Updated Content'} # Data for updating the post.
        response = self.client.put(url, data) # Makes a PUT request to update the post.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Asserts that the response status code is 403 Forbidden.

    def test_like_unlike(self):
        """
        Test liking and unliking a post.
        """
        url_like = reverse('post-like', kwargs={'pk': self.post.pk}) # Gets the URL for the like endpoint.
        url_unlike = reverse('post-unlike', kwargs={'pk': self.post.pk}) # Gets the URL for the unlike endpoint.
        res = self.client.post(url_like) # Makes a POST request to like the post.
        self.assertEqual(res.status_code, status.HTTP_200_OK) # Asserts that the like request was successful.
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists()) # Checks that the like object was created in the database.
        res = self.client.post(url_unlike) # Makes a POST request to unlike the post.
        self.assertEqual(res.status_code, status.HTTP_200_OK) # Asserts that the unlike request was successful.
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists()) # Checks that the like object was deleted from the database.