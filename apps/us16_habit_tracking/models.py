from django.conf import settings
from django.db import models
from django.utils import timezone


class HabitTemplate(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    intention = models.CharField(max_length=140, blank=True)
    category = models.CharField(max_length=40, blank=True)  # e.g. "Body", "Mind"
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return self.name


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )

    # Optional link to a curated template
    template = models.ForeignKey(
        HabitTemplate,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="user_habits",
    )

    name = models.CharField(max_length=80)
    intention = models.CharField(max_length=140, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_active", "name"]

    def __str__(self) -> str:
        return self.name


class HabitLog(models.Model):
    class Status(models.TextChoices):
        DONE = "done", "Done"
        PARTIAL = "partial", "A little"
        NOT_TODAY = "not_today", "Not today"
        NONE = "none", "No entry"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habit_logs",
    )
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NONE)
    reflection = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("habit", "date")
        ordering = ["-date", "habit__name"]

    def __str__(self) -> str:
        return f"{self.habit.name} · {self.date} · {self.status}"