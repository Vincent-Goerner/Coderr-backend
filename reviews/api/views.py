from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Review
from .serializers import ReviewSerializer
from orders.models import Order


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        user = self.request.user

        if not user.userprofile.type == 'customer':
            raise PermissionDenied("Nur Kunden können Bewertungen abgeben.")

        business_user = self.request.data.get("business_user")

        if not business_user:
            raise PermissionDenied("Kein Anbieter angegeben.")

        has_completed_order = Order.objects.filter(customer_user=user,business_user_id=business_user,status="completed").exists()

        if not has_completed_order:
            raise PermissionDenied("Du kannst nur bewerten, wenn du eine abgeschlossene Bestellung bei diesem Anbieter hast.")
        serializer.save(reviewer=user)