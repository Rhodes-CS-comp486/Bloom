from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import HabitForm, HabitLogReflectionForm
from .models import Habit, HabitLog, HabitTemplate


@login_required
def habits_today(request):
    """
    Shows today's active habits and lets user mark status (Done / A little / Not today).
    Ensures a HabitLog exists for each active habit for today.
    """
    today = timezone.localdate()
    habits = Habit.objects.filter(user=request.user, is_active=True)

    existing_logs = HabitLog.objects.filter(user=request.user, date=today, habit__in=habits)
    logs_by_habit_id = {log.habit_id: log for log in existing_logs}

    items = []
    for habit in habits:
        log = logs_by_habit_id.get(habit.id)
        if not log:
            log = HabitLog.objects.create(user=request.user, habit=habit, date=today)
        items.append({"habit": habit, "log": log})

    return render(request, "pages/habits/today.html", {"today": today, "items": items})


@login_required
def habits_manage(request):
    """
    Manage habits:
    - Select multiple habits from the Bloom library (HabitTemplate) and add them.
    - Create a custom habit.
    - View and manage existing habits (pause/remove/edit handled by other endpoints).
    """
    habits = Habit.objects.filter(user=request.user)
    total_templates = HabitTemplate.objects.filter(is_active=True).count()

    existing_template_ids = habits.exclude(template__isnull=True).values_list("template_id", flat=True)
    templates = HabitTemplate.objects.filter(is_active=True).exclude(id__in=existing_template_ids)

    templates_by_category = defaultdict(list)
    for t in templates:
        templates_by_category[t.category or "Other"].append(t)

    added_from_library_count = habits.exclude(template__isnull=True).count()

    if request.method == "POST":
        # 1) Multi-select add from library
        selected_ids = request.POST.getlist("template_ids")
        if selected_ids:
            selected_templates = HabitTemplate.objects.filter(is_active=True, id__in=selected_ids)

            for template in selected_templates:
                Habit.objects.get_or_create(
                    user=request.user,
                    template=template,
                    defaults={
                        "name": template.name,
                        "intention": template.intention,
                        "is_active": True,
                    },
                )

            return redirect("habits_manage")

        # 2) Create custom habit
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("habits_manage")
    else:
        form = HabitForm()

    return render(request, "pages/habits/manage.html", {
        "habits": habits,
        "templates_by_category": dict(templates_by_category),
        "form": form,
        "total_templates": total_templates,
        "added_from_library_count": added_from_library_count,
    })


@login_required
def habit_edit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect("habits_manage")
    else:
        form = HabitForm(instance=habit)

    return render(request, "pages/habits/edit.html", {"form": form, "habit": habit})


@login_required
@require_POST
def habit_pause(request, habit_id):
    """
    Pause a habit (soft remove). Keeps it in 'Your habits' but not shown on Today.
    """
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.is_active = False
    habit.save(update_fields=["is_active"])
    return redirect("habits_manage")


@login_required
@require_POST
def habit_remove(request, habit_id):
    """
    Completely remove the habit.
    (Safe because habits can be re-added from the library.)
    """
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect("habits_manage")


@login_required
def habit_reflection(request, log_id):
    """
    Add/edit a reflection note for a given HabitLog.
    """
    log = get_object_or_404(HabitLog, id=log_id, user=request.user)

    if request.method == "POST":
        form = HabitLogReflectionForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect("habits_today")
    else:
        form = HabitLogReflectionForm(instance=log)

    return render(request, "pages/habits/reflection.html", {"form": form, "log": log})


@login_required
@require_POST
def api_toggle_habit(request, log_id):
    """
    POST: status=done|partial|not_today|none
    Used by Today page buttons.
    """
    log = get_object_or_404(HabitLog, id=log_id, user=request.user)
    status = request.POST.get("status")

    valid = {choice[0] for choice in HabitLog.Status.choices}
    if status not in valid:
        return HttpResponseBadRequest("Invalid status")

    log.status = status
    log.save(update_fields=["status", "updated_at"])
    return JsonResponse({"ok": True, "status": log.status})