from django.urls import path
from .views import ReviewListCreateView, ReviewDetailsView


urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailsView.as_view(), name='review-detail'),
]