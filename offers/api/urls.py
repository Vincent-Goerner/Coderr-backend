from django.urls import path
from .views import OfferListCreateView, OfferDetailView, OfferDetailOverviewView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-details'),
    path('offerdetails/<int:pk>/', OfferDetailOverviewView.as_view(), name='detail-overview'),
]