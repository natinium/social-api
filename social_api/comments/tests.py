from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from posts.models import Post
from rest_framework.authtoken.models import Token
from .models import Comment

class CommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', username='testuser',password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.post = Post.objects.create(author=self.user,title='Post',content='Content')

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'post': self.post.id, 'text': 'Nice post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(post=self.post, user=self.user).exists())