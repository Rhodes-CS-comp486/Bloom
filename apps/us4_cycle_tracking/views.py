from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Cycle

@login_required
def log_period(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")

        if start_date:
            Cycle.objects.create(
                user=request.user,
                start_date=start_date
            )

            profile = request.user.userprofile
            profile.last_period_start = cycle.start_date
            profile.save()

            return redirect("calendar")

    return render(request, "pages/cycle/log_cycle.html")

