from django.urls import path
from . import views

urlpatterns = [
    path("notes/<str:date_str>/", views.notes_for_day, name="notes_for_day"),
    path("notes/<str:date_str>/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("notes/<str:date_str>/<int:note_id>/delete/", views.delete_note, name="delete_note"),
]