from django.db import models
from django.contrib.auth.models import User


class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile = self.user.userprofile
        profile.last_period_start = self.start_date
        profile.save()

    def calculate_length(self):
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None

    def __str__(self):
        return f"{self.user.username} - {self.start_date}"

# Create your models here.



