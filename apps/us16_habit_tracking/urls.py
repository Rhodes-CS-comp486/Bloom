from django.urls import path
from . import views

urlpatterns = [
    path("habits/", views.habits_today, name="habits_today"),
    path("habits/manage/", views.habits_manage, name="habits_manage"),
    path("habits/<int:habit_id>/edit/", views.habit_edit, name="habit_edit"),
    path("habits/log/<int:log_id>/reflection/", views.habit_reflection, name="habit_reflection"),
    path("api/habits/log/<int:log_id>/toggle/", views.api_toggle_habit, name="api_toggle_habit"),

    path("habits/<int:habit_id>/pause/", views.habit_pause, name="habit_pause"),
    path("habits/<int:habit_id>/remove/", views.habit_remove, name="habit_remove"),
]