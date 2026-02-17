from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extended user profile for Bloom-specific data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    date_joined = models.DateTimeField(auto_now_add=True)
    has_completed_onboarding = models.BooleanField(default=False)

    # ✅ US3 fields
    avg_cycle_length = models.PositiveIntegerField(null=True, blank=True)
    last_period_start = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
