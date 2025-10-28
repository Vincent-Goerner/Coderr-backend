from django.db.models import Q
from django.db.models import Min
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from .pagination import StandardResultsSetPagination
from offers.offers_ordering.offers_ordering import OrderingHelperOffers
from offers.models import Offer,OfferDetails
from .serilizers import OfferSerializer, OfferDetailSerializer
from auth_app.models import UserProfile


class OfferListCreateView(ListCreateAPIView):
    """
    API view for listing all offers and creating new ones.
    Supports filtering, search, ordering, and annotated fields like min_price and min_delivery_time.
    Creation is restricted to authenticated business users only.
    """
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        """
        Returns authentication permissions based on request method:
        - POST requires authentication
        - GET is open to any user
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        """
        Returns a filtered and annotated queryset of offers.
        Supports query parameters: creator_id, search, max_delivery_time, min_price, ordering.
        """
        params = self.request.query_params
        offers = Offer.objects.all()

        offers = offers.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )

        if (creator_id := params.get('creator_id')):
            offers = offers.filter(user_id=creator_id)

        if (search := params.get('search', '')):
            offers = offers.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        if (max_delivery_time := params.get('max_delivery_time')):
            try:
                offers = offers.filter(details__delivery_time_in_days__lte=int(max_delivery_time))
            except ValueError:
                raise ValidationError({"max_delivery_time": "Need to be a integer."})
            
        if (min_price := params.get('min_price')):
            try:
                offers = offers.filter(min_price__gte=float(min_price))
            except ValueError:
                raise ValidationError({"min_price": "Need to be a number."})
            
        ordering = params.get('ordering')
        offers = OrderingHelperOffers.apply_ordering(offers, ordering)

        return offers

    def perform_create(self, serializer):
        """
        Validates that the user has a business profile and saves the offer with the current user.
        Raises PermissionDenied if the profile is missing or not a business type.
        """
        user = self.request.user

        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User-profile not found.")

        if profile.type != "business":
            raise PermissionDenied("Only business-user are allowed to create offers.")

        serializer.save(user=user)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single offer.
    Annotates offers with min_price and min_delivery_time for GET responses.
    Update and delete operations are restricted to the offer creator.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        """
        Retrieves a single offer by ID with annotated fields.
        Returns 404 if the offer does not exist.
        """
        offer = get_object_or_404(
            Offer.objects.annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days')
            ),
            pk=pk
        )
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk, format=None):
        """
        Partially updates an offer if the requesting user is the creator.
        Returns 403 if the user is not the owner.
        """

        offer = get_object_or_404(Offer, pk=pk)
        
        if offer.user != request.user:
            raise PermissionDenied("Only the creator can edit the offer.")
        
        serializer = OfferSerializer(offer, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Deletes an offer if the requesting user is the creator.
        Returns 403 if the user is not the owner.
        """
        offer = get_object_or_404(Offer, pk=pk)
        if offer.user != request.user:
            raise PermissionDenied("Only the creator can delete the offer.")

        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class OfferDetailOverviewView(generics.RetrieveAPIView):
    """
    API view to retrieve a single OfferDetail by ID.
    Returns serialized data for the requested offer detail.
    Access restricted to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        offer = get_object_or_404(OfferDetails,pk=pk)
        serializer = OfferDetailSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
