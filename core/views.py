from datetime import date
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render
from core.models import Cycle
from datetime import date

@login_required
def dashboard(request):
    try:
        current_cycle = Cycle.objects.filter(user=request.user).latest("start_date")
        today = date.today()
        day_of_cycle = (today - current_cycle.start_date).days + 1

        cycle_info = {
            "phase_name": "Menstrual",           # example, you can calculate phases later
            "phase_slug": "menstrual",
            "phase_description": "Your period has started.",
            "day_of_cycle": day_of_cycle,
            "days_until_next_period": 28 - day_of_cycle,
        }
    except Cycle.DoesNotExist:
        cycle_info = None

    context = {
        "cycle_info": cycle_info,
        "today": date.today()
    }

    return render(request, "pages/dashboard/dashboard.html", context)
# Create your views here.

@login_required
def calendar_view(request):
    today = date.today()

    # read month/year from query params (e.g. /calendar/?month=2&year=2026)
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    # build month grid (weeks)
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    weeks = cal.monthdatescalendar(year, month)

    # safe prev/next month
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    context = {
        "today": today,
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "weeks": weeks,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }

    return render(request, "pages/calendar/calendar.html", context)
