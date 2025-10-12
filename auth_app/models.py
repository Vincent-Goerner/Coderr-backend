from django.db import models
from django.contrib.auth.models import User
from django.db import models

TYPE_SELECTION = (
    ('business', 'Business'),
    ('customer', 'Customer')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    file = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    working_hours = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=9, choices=TYPE_SELECTION)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil von {self.user.username}"