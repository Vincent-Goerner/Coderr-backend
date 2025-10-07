from django.db import models
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Represents additional profile information linked to a Django User via a one-to-one relationship.
    Used to extend user-related data beyond the default User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the username of the associated user for readable display in admin or logs.
        """
        return self.user.username