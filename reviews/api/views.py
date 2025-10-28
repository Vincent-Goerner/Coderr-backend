from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Review
from .serializers import ReviewSerializer
from orders.models import Order


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    Lists all reviews and allows authenticated customers to create reviews.
    Filters by business_user_id and reviewer_id, supports ordering by updated_at or rating.
    perform_create: ensures only customers with completed orders can review a business_user.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        """
        Validates that the requester is a customer, a business_user is specified,
        and a completed order exists before saving the review.
        """
        user = self.request.user

        if not user.profile.type == 'customer':
            raise PermissionDenied("Only customers can create reviews")

        business_user = self.request.data.get("business_user")

        if not business_user:
            raise PermissionDenied("No provider specified.")

        has_completed_order = Order.objects.filter(customer_user=user,business_user_id=business_user,status="completed").exists()

        if not has_completed_order:
            raise PermissionDenied("You can only rate if you have completed an order with this provider.")
        serializer.save(reviewer=user)


class ReviewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a Review.
    Only the review creator or staff can update or delete.
    GET and PUT methods are explicitly disallowed.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Update a review instance if requester is creator or staff.
        Raises PermissionDenied otherwise.
        """
        if serializer.instance.reviewer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Only the creator or an admin can edit a review.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Delete a review instance if requester is creator or staff.
        Raises PermissionDenied otherwise.
        """
        if instance.reviewer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Only the creator or an admin can delete a review.")
        instance.delete()

    def update(self, request, *args, **kwargs):
        """
        Handles the update request with partial update support.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        """GET method not allowed for this endpoint."""
        raise MethodNotAllowed("GET")
    
    
    def put(self, request, *args, **kwargs):
        """PUT method not allowed for this endpoint."""
        raise MethodNotAllowed("PUT")