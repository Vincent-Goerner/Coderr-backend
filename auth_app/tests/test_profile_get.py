from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from auth_app.api.serializers import UserProfileSerializer

class ProfileTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@email.com", 
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.profile = UserProfile.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_profile_sucessful(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        excepted_data = UserProfileSerializer(self.profile).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, excepted_data)

    def test_get_profile_401(self):
        url = reverse('profile-detail', kwargs={'pk': 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfilTestUnauthorized(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@email.com", 
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_profile_401(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)