from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from auth_app.models import UserProfile
from orders.models import Order


class OrderPatchTest(APITestCase):

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

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Logo Design",
            revisions=2,
            delivery_time_in_days=7,
            price=75,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic",
            status="in_progress"
        )

    def test_patch_order_status_successful(self):
        url = reverse('order-update', kwargs={'pk':self.order.id})
        payload = {
            "status": "completed"
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")
        self.assertEqual(response.data["title"], "Logo Design")
        self.assertEqual(response.data["revisions"], 2)
        self.assertEqual(response.data["delivery_time_in_days"], 7)
        self.assertEqual(float(response.data["price"]), 75.0)
        self.assertEqual(response.data["features"], ["Logo Design", "Visitenkarten"])
        self.assertEqual(response.data["offer_type"], "basic")
        self.assertEqual(response.data["customer_user"], self.customer_user.id)
        self.assertEqual(response.data["business_user"], self.business_user.id)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
    
    def test_patch_order_status_wrong_profile(self):
        url = reverse('order-update', kwargs={'pk':self.order.id})
        payload = {
            "status": "completed"
        }
        self.token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)