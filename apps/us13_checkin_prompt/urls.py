from django.urls import path
from . import views

app_name = "checkin"

urlpatterns = [
    path("dismiss/",  views.dismiss_checkin,  name="dismiss"),
    path("complete/", views.complete_checkin, name="complete"),
    path("refresh/",  views.refresh_prompt,   name="refresh"),
]