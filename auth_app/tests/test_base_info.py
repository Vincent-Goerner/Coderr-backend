from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class BaseInfoTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_base_info(self):
        url = reverse('base-info')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)