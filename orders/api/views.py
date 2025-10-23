from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from orders.models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer
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

class OrderUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def get_permission_classes(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")

        if profile.type != "business":
            raise PermissionDenied("Only business users can update the order status.")

        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        full_data = OrderSerializer(order, context={"request": request}).data
        return Response(full_data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))

        if not request.user.is_staff:
            raise PermissionDenied("Only admins are allowed to delete orders.")
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")
    
    
    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")
    

class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response({"detail": "No business user found with this ID."}, status=404)
        
        order_count = Order.objects.filter(business_user=business_user, status="in_progress").count()
        return Response({"order_count": order_count}, status=200)  
    

class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response({"detail": "No business user found with this ID."}, status=404)
        
        completed_order_count = Order.objects.filter(business_user=business_user, status="completed").count()
        return Response({"completed_order_count": completed_order_count}, status=200)