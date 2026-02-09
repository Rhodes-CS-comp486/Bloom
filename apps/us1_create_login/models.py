from django.contrib.auth.models import User
from django.db import models


# For now, we'll use Django's built-in User model
# Later you can extend it with a UserProfile model like this:

class UserProfile(models.Model):
    """Extended user profile for Bloom-specific data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_joined = models.DateTimeField(auto_now_add=True)
    has_completed_onboarding = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"