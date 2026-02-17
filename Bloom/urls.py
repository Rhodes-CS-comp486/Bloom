from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from core.views import calendar_view


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


@login_required
def dashboard(request):
    return redirect("calendar")


def logout_view(request):
    logout(request)
    return redirect("login")


# Placeholder for login page link
def password_reset(request):
    return redirect("login")


# Placeholders REQUIRED by templates so they don't crash
@login_required
def daily_check_in(request):
    return redirect("calendar")


@login_required
def log_period(request):
    return redirect("calendar")


@login_required
def insights(request):
    return redirect("calendar")


@login_required
def garden(request):
    return redirect("calendar")


@login_required
def settings_view(request):
    return redirect("calendar")


urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL - redirect to login or dashboard
    path('', root_redirect, name='root'),

    # Authentication URLs (login, signup, logout)
    path('', include('apps.us1_create_login.urls')),

    path('', include('apps.us4_cycle_tracking.urls')),

    # Other feature URLs (placeholders for now)
    path('dashboard/', dashboard, name='dashboard'),
    path('onboarding/', onboarding, name='onboarding'),
    path('password-reset/', password_reset, name='password_reset'),
    path('calendar/', calendar_view, name='calendar'),
    path('insights/', insights, name='insights'),
    path('garden/', garden, name='garden'),
    path('settings/', settings_view, name='settings'),
]
    path("admin/", admin.site.urls),

    path("", root_redirect, name="root"),

    # Auth (US1)
    path("", include("apps.us1_create_login.urls")),
    path("logout/", logout_view, name="logout"),
    path("password-reset/", password_reset, name="password_reset"),

    path("", include("apps.us3_start_tracking.urls")),
    # Main pages
    path("dashboard/", dashboard, name="dashboard"),
    path("calendar/", calendar_view, name="calendar"),

    # Placeholder endpoints referenced by templates
    path("check-in/", daily_check_in, name="daily_check_in"),
    path("log-period/", log_period, name="log_period"),
    path("insights/", insights, name="insights"),
    path("garden/", garden, name="garden"),
    path("settings/", settings_view, name="settings"),
]



