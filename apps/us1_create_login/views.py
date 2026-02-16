from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BloomSignupForm, BloomLoginForm
from .models import UserProfile


# ==========================
# LOGIN
# ==========================
def login_view(request):
    # If already logged in, route based on onboarding status
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if not profile.has_completed_onboarding:
            return redirect("onboarding")  # <-- handled by US3 app
        return redirect("calendar")

    if request.method == "POST":
        form = BloomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            profile, _ = UserProfile.objects.get_or_create(user=user)
            if not profile.has_completed_onboarding:
                return redirect("onboarding")  # <-- handled by US3 app

            return redirect("calendar")
    else:
        form = BloomLoginForm()

    return render(request, "pages/auth/login.html", {"form": form})


# ==========================
# SIGNUP
# ==========================
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("calendar")

    if request.method == "POST":
        form = BloomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create profile automatically
            UserProfile.objects.get_or_create(user=user)

            # New users always go to onboarding first (US3)
            return redirect("onboarding")
    else:
        form = BloomSignupForm()

    return render(request, "pages/auth/signup.html", {"form": form})


# ==========================
# LOGOUT
# ==========================
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out. See you soon! 🌸")
    return redirect("login")
