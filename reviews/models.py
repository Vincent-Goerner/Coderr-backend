from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Review(models.Model):
    """
    Represents a review from a user (reviewer) to a business user with rating and description.
    Timestamps track creation and last update automatically.
    Includes string representation and optional update method for saving changes.
    """
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_user")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update(self, **kwargs):
        """
        Overrides save to update the `updated_at` timestamp when called.
        Calls the parent save method with any provided arguments.
        """
        updated_at = now()
        super().save(**kwargs)

    def __str__(self):
        return f"{self.reviewer} reviewed {self.business_user}"