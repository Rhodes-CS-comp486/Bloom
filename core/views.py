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
