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
    """
    API view for listing Orders for the current user and creating new Orders.
    Uses OrderCreateSerializer for POST requests and OrderSerializer for GET requests.
    Only users with a customer profile can create new orders.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method:
        - OrderCreateSerializer for POST requests
        - OrderSerializer for GET requests
        """
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer  

    def get_queryset(self):
        """
        Returns all Orders where the current user is either the customer or the business user.
        Ensures users only see orders relevant to them.
        """
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_create(self, serializer):
        """
        Validates that the current user has a customer profile before creating an Order.
        Raises PermissionDenied if the profile is missing or the user is not a customer.
        Saves the serializer if validation passes.
        """
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")
        if profile.type != "customer":
            raise PermissionDenied("Only customers can create orders.")
        serializer.save()


class OrderUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting Orders: restricts DELETE to admins, updates to business users, forbids GET/PUT.
    get_permission_classes: returns permissions based on request method (DELETE -> admin, else authenticated).
    update/delete: update enforces business-user profile, delete enforces admin; GET/PUT raise MethodNotAllowed.
    """
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def get_permission_classes(self):
        """
        Returns permission classes based on the HTTP method: 
        DELETE requires admin, all other methods require authenticated user.
        """
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """
        Updates an order: only business users can update.
        Validates request data and returns the full serialized order.
        Raises PermissionDenied if user profile is missing or not business type.
        """
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
        """
        Deletes an order: only admins are allowed.
        Raises PermissionDenied if the requesting user is not staff.
        Returns HTTP 204 on successful deletion.
        """
        order = get_object_or_404(Order, pk=kwargs.get("pk"))

        if not request.user.is_staff:
            raise PermissionDenied("Only admins are allowed to delete orders.")
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, *args, **kwargs):
        """
        GET method is not allowed for this view.
        Raises MethodNotAllowed.
        """
        raise MethodNotAllowed("GET")
    
    
    def put(self, request, *args, **kwargs):
        """
        PUT method is not allowed for this view.
        Raises MethodNotAllowed.
        """
        raise MethodNotAllowed("PUT")
    

class OrderCountView(APIView):
    """
    Returns the count of 'in_progress' orders for a specific business user.
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Retrieves the number of orders with status 'in_progress' for the given business user ID.
        Returns 404 if the business user does not exist.
        """
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response({"detail": "No business user found with this ID."}, status=404)
        
        order_count = Order.objects.filter(business_user=business_user, status="in_progress").count()
        return Response({"order_count": order_count}, status=200)  
    

class CompletedOrderCountView(APIView):
    """
    Returns the count of 'completed' orders for a specific business user.
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Retrieves the number of orders with status 'completed' for the given business user ID.
        Returns 404 if the business user does not exist.
        """
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            return Response({"detail": "No business user found with this ID."}, status=404)
        
        completed_order_count = Order.objects.filter(business_user=business_user, status="completed").count()
        return Response({"completed_order_count": completed_order_count}, status=200)