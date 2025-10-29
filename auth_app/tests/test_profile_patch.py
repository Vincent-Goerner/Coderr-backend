from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class ProfilePatchTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.profile = UserProfile.objects.create(user=self.user)

        self.second_user = User.objects.create_user(
            username="2",
            email="test@email222.com",
            password="testpassword2222"
        )
        self.second_token = Token.objects.create(user=self.second_user)
        self.profile = UserProfile.objects.create(user=self.second_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_patch_profile_sucessful(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        patch_data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Dresden",
            "email": "user@email.com",
            "tel": "28374892374"
        }
        response = self.client.patch(url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Max")
        self.assertEqual(response.data["last_name"], "Mustermann")
        self.assertEqual(response.data["location"], "Dresden")
        self.assertEqual(response.data["email"], "user@email.com")
        self.assertEqual(response.data["tel"], "28374892374")        

    def test_patch_profile_404(self):
        url = reverse('profile-detail', kwargs={'pk': 9999})
        patch_data = {
            "username": "testuser2"
        }
        response = self.client.patch(url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_profile_403(self):
        url = reverse('profile-detail', kwargs={'pk': self.second_user.id})
        patch_data = {
            "username": "testuser2"
        }
        response = self.client.patch(url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfilPatchTestUnauthorized(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@email.com", 
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_patch_profile_401(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)