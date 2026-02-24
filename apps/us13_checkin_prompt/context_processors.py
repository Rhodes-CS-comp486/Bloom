"""
checkin/context_processors.py

Inject daily check-in context into every template automatically.

Register in settings.py → TEMPLATES[0]['OPTIONS']['context_processors']:
    'checkin.context_processors.daily_checkin',
"""

from .views import get_checkin_context


def daily_checkin(request):
    """
    Makes `show_checkin` and `checkin` available in every template.
    Skips gracefully for unauthenticated users and non-HTML requests (e.g. API).
    """
    if not request.user.is_authenticated:
        return {"show_checkin": False, "checkin": None}

    # Avoid running on AJAX/fetch calls that already came FROM the card
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return {}

    return get_checkin_context(request.user)