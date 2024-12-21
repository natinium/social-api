from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from .models import Post, Like
from rest_framework.authtoken.models import Token

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123')
        self.post = Post.objects.create(author=self.user,title='Test Post',content='Test Content')
    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))

class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.post = Post.objects.create(author=self.user,title='Test Post',content='Test Content')

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_post_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_create(self):
        url = reverse('post-list')
        data = {'title': 'New Post','content': 'New Content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Post','content': 'Updated Content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_post_create(self):
        self.client.credentials()
        url = reverse('post-list')
        data = {'title': 'New Post','content': 'New Content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_post_update(self):
        other_user = User.objects.create_user(email='other@test.com',username='otheruser',password='testpass123')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Post','content': 'Updated Content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_unlike(self):
        url_like = reverse('post-like', kwargs={'pk': self.post.pk})
        url_unlike = reverse('post-unlike', kwargs={'pk': self.post.pk})
        res = self.client.post(url_like)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())
        res = self.client.post(url_unlike)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())