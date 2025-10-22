from django.urls import path
from .views import OrderListCreateView, OrderUpdateDeleteView


urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderUpdateDeleteView.as_view(), name='order-update'),
]