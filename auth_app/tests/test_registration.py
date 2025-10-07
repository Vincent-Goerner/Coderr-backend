from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class RegistrationTest(APITestCase):

    def test_post_registration(self):
        url = reverse('registration')
        self.token = Token.objects.create(user=self.user)
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'token': self.token
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)