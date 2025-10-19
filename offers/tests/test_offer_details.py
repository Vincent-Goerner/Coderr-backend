from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from offers.models import OfferDetails, Offer


class OfferDetailsGetTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.profile = UserProfile.objects.create(user=self.user, type="business")
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
        

    def test_get_offer_details(self):
        url = reverse('offer-details', kwargs={'pk': self.detail.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.detail.id)
        self.assertEqual(response.data["title"], self.detail.title)


class OfferDetailsPatchTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.profile = UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.offer = Offer.objects.create(
            user=self.user, 
            title="Test Offer", 
            description="Test Offer Description"
        )
        self.details = OfferDetails.objects.create(
            offer = self.offer,
            title = "Test Offer",
            revisions=2,
            delivery_time_in_days=7, 
            price=75,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )

    def test_patch_offer_details_successful(self):
        url = reverse('offer-details', kwargs={'pk': self.details.id})
        payload = {
            "title": "Updated Test-Paket",
            "details": [
                {
                "title": "Basic Test Updated",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 150,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "basic"
                },
                {
                "title": "Basic Test Updated",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 150,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "standard"
                },
                {
                "title": "Basic Test Updated",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 150,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "premium"
                }
            ]
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Test-Paket")

        for detail in response.data["details"]:
            self.assertIn("id", detail)
            self.assertIn("url", detail)
            
    def test_patch_offer_details_403(self):
        not_creator = User.objects.create_user(username="Not Owner", password="testpass")
        UserProfile.objects.create(user=not_creator, type="business")
        other_token = Token.objects.create(user=not_creator)
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)

        url = reverse('offer-details', kwargs={'pk':self.details.id})
        payload = {
            "title": "Updated Test-Paket",
            "details": [
                {
                "title": "Basic Test Updated",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 150,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "basic"
                },
                {
                "title": "Basic Test Updated",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 150,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "standard"
                },
                {
                "title": "Basic Test Updated",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 150,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "premium"
                }
            ]
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class OfferDetailsDeleteTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword"
        )
        self.profile = UserProfile.objects.create(user=self.user, type="business")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.offer = Offer.objects.create(
            user=self.user, 
            title="Test Offer", 
            description="Test Offer Description"
        )
        self.details = OfferDetails.objects.create(
            offer = self.offer,
            title = "Test Offer",
            revisions=2,
            delivery_time_in_days=7, 
            price=75,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )

    def test_delete_offer_details_successful(self):
        url = reverse('offer-details', kwargs={'pk':self.details.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_offer_details_403(self):
        not_creator = User.objects.create_user(username="Not Owner", password="testpass")
        UserProfile.objects.create(user=not_creator, type="business")
        other_token = Token.objects.create(user=not_creator)
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)

        url = reverse('offer-details', kwargs={'pk':self.details.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)