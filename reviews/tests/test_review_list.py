from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from auth_app.models import UserProfile
from reviews.models import Review
from offers.models import Offer, OfferDetails
from orders.models import Order


class ReviewListGetTest(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="Business",
            email="business@email.com",
            password="testpassword1"
        )
        self.profile = UserProfile.objects.create(user=self.business_user, type="business")
        self.token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.customer_user = User.objects.create_user(
            username="Customer",
            email="customer@email.com",
            password="testpassword2"
        )
        self.profile = UserProfile.objects.create(user=self.customer_user, type="customer")

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr professioneller Service."
        )

    def test_get_review_list(self):
        url = reverse('review-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)


class ReviewListPostTest(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="Customer",
            email="customer@email.com",
            password="testpassword2"
        )
        self.profile = UserProfile.objects.create(user=self.customer_user, type="customer")
        self.token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.business_user = User.objects.create_user(
            username="Business",
            email="business@email.com",
            password="testpassword1"
        )
        self.profile = UserProfile.objects.create(user=self.business_user, type="business")

        self.offer = Offer.objects.create(
            user=self.business_user, 
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

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Logo Basic",
            revisions=3,
            delivery_time_in_days=7,
            price=150,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic",
            status="completed"
        )

    def test_post_review_list(self):
        url = reverse('review-list')
        payload = {
            'business_user': self.business_user.id,
            'rating': 4,
            'description': 'Sehr professioneller Service.'
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["business_user"], self.business_user.id)
        self.assertEqual(response.data["reviewer"], self.customer_user.id)
        self.assertEqual(response.data["rating"], 4)
        self.assertEqual(response.data["description"], "Sehr professioneller Service.")