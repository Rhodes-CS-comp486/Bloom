from django import forms
from .models import DayNote


class DayNoteForm(forms.ModelForm):
    class Meta:
        model = DayNote
        fields = ["title", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Optional title"}),
            "body": forms.Textarea(attrs={
                "rows": 7,
                "placeholder": "What would you like to remember from this day?",
            }),
        }