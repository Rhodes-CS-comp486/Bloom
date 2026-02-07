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
from django.urls import path
from django.http import HttpResponse

# Import your login view
try:
    from apps.us1_create_login import views as auth_views
except ImportError:
    # If the app doesn't exist yet, create a placeholder
    from django.shortcuts import render
    class auth_views:
        @staticmethod
        def login_view(request):
            return render(request, 'pages/auth/login.html')

# Placeholder functions for links in templates
def password_reset(request):
    return HttpResponse("<h1>Password Reset</h1><p>Coming soon!</p>")

def signup(request):
    return HttpResponse("<h1>Sign Up</h1><p>Coming soon!</p>")

def dashboard(request):
    return HttpResponse("<h1>Dashboard</h1><p>Coming soon!</p>")

def calendar_view(request):
    return HttpResponse("<h1>Calendar</h1><p>Coming soon!</p>")

def insights(request):
    return HttpResponse("<h1>Insights</h1><p>Coming soon!</p>")

def garden(request):
    return HttpResponse("<h1>Garden</h1><p>Coming soon!</p>")

def settings_view(request):
    return HttpResponse("<h1>Settings</h1><p>Coming soon!</p>")

def logout_view(request):
    return HttpResponse("<h1>Logged Out</h1><p>You've been logged out.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.login_view, name='login'),
    path('password-reset/', password_reset, name='password_reset'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('calendar/', calendar_view, name='calendar'),
    path('insights/', insights, name='insights'),
    path('garden/', garden, name='garden'),
    path('settings/', settings_view, name='settings'),
    path('logout/', logout_view, name='logout'),
]