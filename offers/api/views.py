from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Min
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.exceptions import ValidationError
from .pagination import StandardResultsSetPagination
from offers.offers_ordering.offers_ordering import OrderingHelperOffers
from offers.models import Offer,OfferDetails
from .serilizers import OfferSerializer, OfferDetailSerializer
from auth_app.models import UserProfile


class OfferListCreateView(ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Offer.objects.all()
        content_params = self.request.query_params
        creator_id = content_params.get('creator_id', None)
        search = content_params.get('search', '')
        max_delivery_time = content_params.get('max_delivery_time', None)
        min_price = content_params.get('min_price', None)

        queryset = queryset.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )

        if creator_id is not None:
            queryset = queryset.filter(user_id=creator_id)

        if search is not '':
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        if max_delivery_time is not None:
            try:
                queryset = queryset.filter(details__delivery_time_in_days__lte=int(max_delivery_time))
            except ValueError:
                raise ValidationError({"max_delivery_time": "Need to be a integer."})
            
        if min_price is not None:
            try:
                queryset = queryset.filter(min_price__gte=float(min_price))
            except ValueError:
                raise ValidationError({"min_price": "Need to be from type number."})
        
        ordering = content_params.get('ordering')
        queryset = OrderingHelperOffers.apply_ordering(queryset, ordering)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User-profile not found.")

        if profile.type != "business":
            raise PermissionDenied("Only business-user are allowed to create offers.")

        serializer.save(user=user)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
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
        offer = get_object_or_404(Offer, pk=pk)
        
        if offer.user != request.user:
            raise PermissionDenied("Only the creator can edit the offer.")
        
        serializer = OfferSerializer(offer, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        offer = get_object_or_404(Offer, pk=pk)
        if offer.user != request.user:
            raise PermissionDenied("Only the creator can delete the offer.")

        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OfferDetailOverviewView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        offer = get_object_or_404(OfferDetails,pk=pk)
        serializer = OfferDetailSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
