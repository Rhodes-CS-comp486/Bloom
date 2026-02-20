import random
from django.contrib.auth.decorators import login_required
from django.http  import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import DailyCheckIn

# ── Prompt bank ───────────────────────────────────────────────────────────────
# Add, remove, or load from DB however you like.
PROMPTS = [
    "What's one thing you're looking forward to today?",
    "How are you feeling going into today?",
    "What's something you accomplished yesterday that you're proud of?",
    "What's your main focus for today?",
    "Is there anything on your mind that you'd like to clear before starting?",
    "What would make today feel like a success?",
    "How's your energy level right now?",
    "What's one small win you can aim for today?",
    "Is there anything you need support with today?",
    "What intention do you want to set for today?",
    "How did yesterday go, and what would you do differently?",
    "What are you grateful for this morning?",
    "What's one challenge you're anticipating today?",
    "How are you taking care of yourself today?",
    "What's something you've been putting off that you could tackle today?",
]


def _pick_prompt(exclude_text=None):
    """Return a random prompt, optionally avoiding the currently shown one."""
    pool = [p for p in PROMPTS if p != exclude_text] or PROMPTS
    return random.choice(pool)


# ── Context helper (call from your base view or context processor) ─────────────

def get_checkin_context(user):
    """
    Returns a dict ready to pass into any template context:
        {
            'show_checkin': True/False,
            'checkin':      DailyCheckIn instance | None,
        }

    Usage in a view:
        context.update(get_checkin_context(request.user))
    """
    if not user.is_authenticated:
        return {"show_checkin": False, "checkin": None}

    today   = timezone.localdate()
    checkin = DailyCheckIn.objects.filter(user=user, date=today).first()

    if checkin is None:
        # First visit today – create a pending record
        checkin = DailyCheckIn.objects.create(
            user        = user,
            date        = today,
            prompt_text = _pick_prompt(),
        )

    return {
        "show_checkin": checkin.is_actionable,
        "checkin":      checkin,
    }


# ── AJAX endpoints ─────────────────────────────────────────────────────────────

@login_required
@require_POST
def dismiss_checkin(request):
    """Dismiss today's prompt without answering."""
    today   = timezone.localdate()
    checkin = DailyCheckIn.objects.filter(user=request.user, date=today).first()

    if checkin and checkin.is_actionable:
        checkin.dismiss()

    return JsonResponse({"status": "dismissed"})


@login_required
@require_POST
def complete_checkin(request):
    """Save the user's response and mark as completed."""
    today    = timezone.localdate()
    response = request.POST.get("response", "").strip()
    checkin  = DailyCheckIn.objects.filter(user=request.user, date=today).first()

    if checkin and checkin.is_actionable:
        checkin.complete(response_text=response)
        return JsonResponse({"status": "completed"})

    return JsonResponse({"status": "already_resolved"})


@login_required
@require_POST
def refresh_prompt(request):
    """Swap today's prompt for a new random question (without resolving the check-in)."""
    today   = timezone.localdate()
    checkin = DailyCheckIn.objects.filter(user=request.user, date=today).first()

    if checkin and checkin.is_actionable:
        checkin.prompt_text = _pick_prompt(exclude_text=checkin.prompt_text)
        checkin.save(update_fields=["prompt_text", "updated_at"])
        return JsonResponse({"status": "ok", "prompt": checkin.prompt_text})

    return JsonResponse({"status": "not_actionable"}, status=400)