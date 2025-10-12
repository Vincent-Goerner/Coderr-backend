from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class RegistrationTest(APITestCase):

    def test_post_registration(self):
        url = reverse('registration')
        payload = {
            'username': 'testuser',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'email': 'test@email.com',
            'type': 'customer'
        }
        response = self.client.post(url, payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertIn("token", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("user_id", response.data)
