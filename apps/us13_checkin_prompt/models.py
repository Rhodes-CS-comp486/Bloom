from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DailyCheckIn(models.Model):
    """
    Tracks one check-in record per user per day.
    A record is created the first time the prompt is shown.
    Status transitions: pending → dismissed | completed
    """

    STATUS_PENDING   = "pending"
    STATUS_DISMISSED = "dismissed"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_PENDING,   "Pending"),
        (STATUS_DISMISSED, "Dismissed"),
        (STATUS_COMPLETED, "Completed"),
    ]

    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkins")
    date          = models.DateField(default=timezone.localdate)
    status        = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    prompt_text   = models.TextField()                        # the question shown that day
    response_text = models.TextField(blank=True, default="") # user's answer (if completed)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "date")   # enforces one record per user per day
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} – {self.date} [{self.status}]"

    # ── convenience helpers ───────────────────────────────────────────────────

    @property
    def is_actionable(self):
        """True when the prompt should still be shown (not yet resolved)."""
        return self.status == self.STATUS_PENDING

    def dismiss(self):
        self.status = self.STATUS_DISMISSED
        self.save(update_fields=["status", "updated_at"])

    def complete(self, response_text=""):
        self.status        = self.STATUS_COMPLETED
        self.response_text = response_text
        self.save(update_fields=["status", "response_text", "updated_at"])