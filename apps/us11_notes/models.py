from django.conf import settings
from django.db import models


class DayNote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="day_notes",
    )
    date = models.DateField(db_index=True)

    title = models.CharField(max_length=120, blank=True)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # multiple notes per day -> no unique constraint
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.user} - {self.date} ({self.id})"