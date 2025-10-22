from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from auth_app.models import UserProfile
from offers.models import Offer, OfferDetails


class OrderGetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.profile = UserProfile.objects.create(user=self.user, type="customer")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_order_list(self):
        url = reverse('order-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderPostTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.profile = UserProfile.objects.create(user=self.user, type="customer")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        
        self.offer = Offer.objects.create(
            user=self.user, 
            title="Test Offer", 
            description="Test Offer Description"
        )
        self.detail = OfferDetails.objects.create(
            offer = self.offer,
            title = "Test Offer",
            revisions=2,
            delivery_time_in_days=7, 
            price=75,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )

    def test_post_order_list(self):
        url = reverse('order-list')
        payload = {
            "offer_detail_id": self.detail.id
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)