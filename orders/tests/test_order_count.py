from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from auth_app.models import UserProfile
from orders.models import Order


class OrderCountTest(APITestCase):

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

    def test_get_order_count(self):
        url = reverse('order-count', kwargs={'business_user_id':self.business_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1)


class OrderCompletedCountTest(APITestCase):

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
            status="completed"
        )

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Logo Design",
            revisions=2,
            delivery_time_in_days=7,
            price=75,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic",
            status="completed"
        )

    def test_get_order_completed_count(self):
        url = reverse('order-completed-count', kwargs={'business_user_id':self.business_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 2)

