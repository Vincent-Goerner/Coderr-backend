from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from orders.models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from auth_app.models import UserProfile


class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer  

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_create(self, serializer):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")
        if profile.type != "customer":
            raise PermissionDenied("Only customers can create orders.")
        serializer.save()