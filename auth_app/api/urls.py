from django.urls import path
from .views import RegistrationView, CustomLoginView, ProfileDetailView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/business/', BusinessProfileListView.as_view(), name='business-list'),
    path('profile/customer/', CustomerProfileListView.as_view(), name='customer-list'),
]