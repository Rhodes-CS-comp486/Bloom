from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .forms import DayNoteForm
from .models import DayNote


def _parse_day(date_str: str):
    day = parse_date(date_str)
    if not day:
        raise ValueError("Invalid date")
    return day


@login_required
def notes_for_day(request, date_str):
    """
    List notes for a day + create a new note for that day.
    URL: /notes/YYYY-MM-DD/
    """
    day = _parse_day(date_str)

    if request.method == "POST":
        # Create a NEW note each time (no instance passed)
        form = DayNoteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date = day
            obj.save()
            return redirect("notes_for_day", date_str=date_str)
    else:
        form = DayNoteForm()

    notes = DayNote.objects.filter(user=request.user, date=day).order_by("-created_at")

    return render(request, "pages/notes/day_notes.html", {
        "day": day,
        "form": form,
        "notes": notes,
    })


@login_required
def edit_note(request, date_str, note_id):
    """
    Edit one specific note.
    URL: /notes/YYYY-MM-DD/<id>/edit/
    """
    day = _parse_day(date_str)
    note = get_object_or_404(DayNote, id=note_id, user=request.user, date=day)

    if request.method == "POST":
        form = DayNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes_for_day", date_str=date_str)
    else:
        form = DayNoteForm(instance=note)

    return render(request, "pages/notes/edit_note.html", {
        "day": day,
        "note": note,
        "form": form,
    })


@login_required
@require_POST
def delete_note(request, date_str, note_id):
    """
    Delete one specific note.
    URL: /notes/YYYY-MM-DD/<id>/delete/
    """
    day = _parse_day(date_str)
    note = get_object_or_404(DayNote, id=note_id, user=request.user, date=day)
    note.delete()
    return redirect("notes_for_day", date_str=date_str)