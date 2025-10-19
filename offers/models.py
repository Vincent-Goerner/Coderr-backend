from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers_pics/", null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetails(models.Model):
    PAKET_TYPES = (
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    )

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=8, choices=PAKET_TYPES)
    
    def __str__(self):
        return f"{self.offer.title} - {self.title}"