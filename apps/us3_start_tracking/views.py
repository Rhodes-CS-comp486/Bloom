from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.us1_create_login.models import UserProfile
from .forms import StartTrackingForm


@login_required
def onboarding_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # allow existing users to revisit onboarding via /onboarding/?edit=1
    edit_mode = request.GET.get("edit") == "1"

    # if onboarding already done and not editing, send them to calendar
    if profile.has_completed_onboarding and not edit_mode:
        return redirect("calendar")

    if request.method == "POST":
        form = StartTrackingForm(request.POST)
        if form.is_valid():
            profile.avg_cycle_length = form.cleaned_data["avg_cycle_length"]
            profile.last_period_start = form.cleaned_data["last_period_start"]
            profile.has_completed_onboarding = True
            profile.save()
            return redirect("calendar")
    else:
        # prefill the form for editing / returning users
        form = StartTrackingForm(initial={
            "avg_cycle_length": profile.avg_cycle_length,
            "last_period_start": profile.last_period_start,
        })

    return render(request, "pages/onboarding/onboarding.html", {"form": form, "edit_mode": edit_mode})
