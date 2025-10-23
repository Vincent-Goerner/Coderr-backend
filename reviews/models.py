from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_user")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update(self, **kwargs):
        updated_at = now()
        super().save(**kwargs)

    def __str__(self):
        return f"{self.reviewer} reviewed {self.business_user}"