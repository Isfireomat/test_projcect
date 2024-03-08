from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.account_url = reverse('account')
        self.user = User.objects.create_user(username='testuser', password='1234567890', email='test@gmail.com')
        refresh_token = RefreshToken.for_user(self.user)
        self.access_token=str(refresh_token.access_token)
        self.refresh_token=str(refresh_token)
        self.user_auth={
            'username': 'newtestuser',
            'email': 'newtestuser@gmail.com',
            'password': '1234567890'
        }
        
    def test_register_view_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp1/reg.html')

    def test_register_view_POST(self):
        response = self.client.post(self.register_url, self.user_auth)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp1/login.html')

    def test_login_view_POST(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': '1234567890'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/')

    def test_account_view_GET(self):
        self.client.cookies['refresh_token'] = self.refresh_token
        self.client.cookies['access_token'] = self.access_token
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp1/user_acc.html')

    def test_account_view_POST(self):
        self.client.cookies['refresh_token'] = self.refresh_token
        response = self.client.post(self.account_url, {'logout': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')