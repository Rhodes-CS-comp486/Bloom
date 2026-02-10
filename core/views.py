from datetime import date
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
