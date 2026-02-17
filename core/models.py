from django.db import models
from django.contrib.auth.models import User


class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.start_date}"

# Create your models here.



