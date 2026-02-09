"""
URL configuration for Bloom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect


# Redirect root to login
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


# Placeholder views for features not yet implemented
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return HttpResponse(f"<h1>Dashboard</h1><p>Welcome {request.user.username}! Coming soon!</p>")


def onboarding(request):
    return HttpResponse("<h1>Onboarding</h1><p>Coming soon!</p>")


def password_reset(request):
    return HttpResponse("<h1>Password Reset</h1><p>Coming soon!</p>")


def calendar_view(request):
    return HttpResponse("<h1>Calendar</h1><p>Coming soon!</p>")


def insights(request):
    return HttpResponse("<h1>Insights</h1><p>Coming soon!</p>")


def garden(request):
    return HttpResponse("<h1>Garden</h1><p>Coming soon!</p>")


def settings_view(request):
    return HttpResponse("<h1>Settings</h1><p>Coming soon!</p>")


urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL - redirect to login or dashboard
    path('', root_redirect, name='root'),

    # Authentication URLs (login, signup, logout)
    path('', include('apps.us1_create_login.urls')),

    # Other feature URLs (placeholders for now)
    path('dashboard/', dashboard, name='dashboard'),
    path('onboarding/', onboarding, name='onboarding'),
    path('password-reset/', password_reset, name='password_reset'),
    path('calendar/', calendar_view, name='calendar'),
    path('insights/', insights, name='insights'),
    path('garden/', garden, name='garden'),
    path('settings/', settings_view, name='settings'),
]