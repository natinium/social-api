from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Follow
from rest_framework.authtoken.models import Token

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com',username='testuser',password='testpass123')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertTrue(self.user.check_password('testpass123'))

class UserAPITest(APITestCase):
    def setUp(self):
        self.user_data = {'email': 'test@test.com','username': 'testuser','password': 'testpass123'}
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_user_registration_success(self):
        url = reverse('user-register')
        data = {'email': 'new@test.com','username': 'newuser','password': 'newpass123','password2': 'newpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(email='new@test.com').exists())

    def test_user_registration_password_mismatch(self):
        url = reverse('user-register')
        data = {'email': 'new@test.com','username': 'newuser','password': 'newpass123','password2': 'diff'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        url = reverse('user-register')
        data = {'email': 'test@test.com','username': 'newuser','password': 'newpass123','password2': 'newpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        url = reverse('user-login')
        data = {'email': 'test@test.com','password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid_credentials(self):
        url = reverse('user-login')
        data = {'email': 'test@test.com','password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_nonexistent_user(self):
        url = reverse('user-login')
        data = {'email': 'nonexistent@test.com','password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_unfollow(self):
        other = User.objects.create_user(email='other@test.com',username='otheruser',password='pass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        follow_url = reverse('user-follow', kwargs={'pk': other.pk})
        unfollow_url = reverse('user-unfollow', kwargs={'pk': other.pk})

        # follow
        res = self.client.post(follow_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(Follow.objects.filter(follower=self.user, following=other).exists())

        # unfollow
        res = self.client.post(unfollow_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(follower=self.user, following=other).exists())