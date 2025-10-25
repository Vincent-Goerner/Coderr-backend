from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from auth_app.models import UserProfile
from reviews.models import Review
from offers.models import Offer, OfferDetails
from orders.models import Order


class ReviewDetailTest(APITestCase):

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

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr professioneller Service."
        )
    
    def test_patch_review_detail(self):
        url = reverse('review-detail', kwargs={'pk':self.review.id})
        payload = {
            'rating': 5,
            'description': 'Hervoragende Arbeit'
        }
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["description"], "Hervoragende Arbeit")