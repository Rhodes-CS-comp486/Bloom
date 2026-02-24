from django.contrib import admin
from .models import HabitTemplate, Habit, HabitLog


@admin.register(HabitTemplate)
class HabitTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "sort_order", "slug")
    list_filter = ("is_active", "category")
    search_fields = ("name", "intention", "slug")
    ordering = ("sort_order", "name")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_active", "template")
    list_filter = ("is_active",)
    search_fields = ("name", "intention", "user__username", "user__email")


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ("habit", "user", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("habit__name", "user__username", "user__email")