from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class ProfileGetBusinessProfilesTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.buisness_profile = UserProfile.objects.create(
            user=self.user,
            type='business',
            location='Sachsen'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_business_profiles(self):
        url = reverse('business-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        usernames = [profile['username'] for profile in response.data]
        self.assertIn(self.user.username, usernames)

        for profile in response.data:
            self.assertEqual(profile['type'], 'business')
