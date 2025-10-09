from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class LoginTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@email.com", 
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_post_login_successful(self):
        url = reverse('login')
        data = {
            'username': self.user.username,
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data['token'], self.token.key)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['user_id'], self.user.id)