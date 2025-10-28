from django.urls import path
from .views import RegistrationView, CustomLoginView, ProfileDetailView, BusinessProfileListView, CustomerProfileListView, BaseInfoView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfileListView.as_view(), name='business-list'),
    path('profiles/customer/', CustomerProfileListView.as_view(), name='customer-list'),
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]