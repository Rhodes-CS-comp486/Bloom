from django.urls import path
from . import views

urlpatterns = [
    path("log-period/", views.log_period, name="log_period"),
]

