from django.db import models
from django.contrib.auth.models import User


class Order (models.Model):
    
    PAKET_TYPES = (
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    )

    STATUS = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    )

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cutsomer_user')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_user')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=8, choices=PAKET_TYPES)
    status = models.CharField(max_length=12, choices=STATUS, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)