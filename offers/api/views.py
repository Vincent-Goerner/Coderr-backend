from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Min
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
from offers.models import Offer
from .serilizers import OfferSerializer
from auth_app.models import UserProfile


class OfferListCreateView(ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
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
                raise ValidationError({"max_delivery_time": "Muss eine ganze Zahl sein."})
            
        if (min_price := params.get('min_price')):
            try:
                offers = offers.filter(min_price__gte=float(min_price))
            except ValueError:
                raise ValidationError({"min_price": "Muss eine Zahl sein."})
            
        ordering = params.get('ordering')
        offers = OrderingHelperOffers.apply_ordering(offers, ordering)

        return offers

    def perform_create(self, serializer):
        user = self.request.user

        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("Kein UserProfile gefunden.")

        if profile.type != "business":
            raise PermissionDenied("Nur Business-User dürfen Angebote erstellen.")

        serializer.save(user=user)