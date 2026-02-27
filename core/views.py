# core/views.py
from datetime import date, timedelta
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.utils import OperationalError

from core.models import Cycle

# US11 Notes model
try:
    from apps.us11_notes.models import DayNote
except Exception:
    DayNote = None


@login_required
def dashboard(request):
    """
    Dashboard shows a simple snapshot of current cycle info.
    """
    try:
        current_cycle = Cycle.objects.filter(user=request.user).latest("start_date")
        today = date.today()

        # If period ended, use actual length, otherwise compute days since start.
        if current_cycle.end_date:
            period_length = current_cycle.calculate_length()
            day_of_cycle = period_length
        else:
            day_of_cycle = (today - current_cycle.start_date).days + 1
            period_length = day_of_cycle

        cycle_info = {
            "phase_name": "Menstrual",
            "phase_slug": "menstrual",
            "phase_description": "Your period has started.",
            "day_of_cycle": day_of_cycle,
            "period_length": period_length,
            "days_until_next_period": max(0, 28 - day_of_cycle),
        }
    except Cycle.DoesNotExist:
        cycle_info = None

    context = {
        "cycle_info": cycle_info,
        "today": date.today(),
    }
    return render(request, "pages/dashboard/dashboard.html", context)


@login_required
def calendar_view(request):
    """
    Calendar month view:
    - shows the month grid
    - highlights period days
    - shows note indicators and previews
    """
    today = date.today()

    # read month/year from query params (e.g. /calendar/?month=2&year=2026)
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    # build month grid (weeks)
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    weeks = cal.monthdatescalendar(year, month)

    # collect period days for the visible month
    user_cycles = Cycle.objects.filter(user=request.user)
    period_days = set()

    for cycle in user_cycles:
        start = cycle.start_date
        # assume 5-day period if no end_date provided
        end = cycle.end_date if cycle.end_date else (start + timedelta(days=4))

        current = start
        while current <= end:
            if current.month == month and current.year == year:
                period_days.add(current)
            current += timedelta(days=1)

    # safe prev/next month
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    # Notes for this month
    note_dates = set()
    notes_for_month = []

    if DayNote is not None:
        try:
            note_qs = DayNote.objects.filter(
                user=request.user,
                date__year=year,
                date__month=month,
            ).order_by("-created_at")

            notes_for_month = list(note_qs)
            note_dates = {n.date for n in notes_for_month}
        except OperationalError:
            # Table not migrated yet -> keep notes empty instead of crashing
            note_dates = set()
            notes_for_month = []

    context = {
        "today": today,
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "weeks": weeks,
        "period_days": period_days,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "note_dates": note_dates,
        "notes_for_month": notes_for_month,
    }

    return render(request, "pages/calendar/calendar.html", context)