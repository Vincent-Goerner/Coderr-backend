from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from offers.models import Offer, OfferDetails


class OfferListTest(APITestCase):
    
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

        first_offer = Offer.objects.create(user=self.user, title="Tech Design", description="Nice tech design.")
        OfferDetails.objects.create(offer=first_offer, offer_type="basic", price=100, delivery_time_in_days=5, revisions=1, features=["Add Feature here"])
        OfferDetails.objects.create(offer=first_offer, offer_type="standard", price=150, delivery_time_in_days=7, revisions=1, features=["Add more Feature here"])
        OfferDetails.objects.create(offer=first_offer, offer_type="premium", price=250, delivery_time_in_days=10, revisions=1, features=["You really need to add Feature here"])

    def test_get_offer_list(self):
        url = reverse('offer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_offer_list(self):
        url = reverse('offer-list')
        payload = {
            'title':'Nicer Designs',
            'description':'Pretty Nice tech design.',
            'details':[
                {
                    'offer_type':'basic', 'price':250, 'delivery_time_in_days':4, 'revisions':1, 'features':['Add Feature here']
                },
                {
                    'offer_type':'standard', 'price':350, 'delivery_time_in_days':8, 'revisions':1, 'features':['Add more Feature here']
                },
                {
                    'offer_type':'premium', 'price':500, 'delivery_time_in_days':14, 'revisions':1, 'features':['You really need to add Feature here']
                }
            ]
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
