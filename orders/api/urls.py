from django.urls import path
from .views import OrderListCreateView, OrderUpdateDeleteView, OrderCountView, CompletedOrderCountView


urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderUpdateDeleteView.as_view(), name='order-update'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='order-completed-count'),
]