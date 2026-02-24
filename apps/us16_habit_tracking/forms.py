from django import forms
from .models import Habit, HabitLog


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "intention", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g., Drink water"}),
            "intention": forms.TextInput(attrs={"class": "form-input", "placeholder": "Optional: why this supports you"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }


class HabitLogReflectionForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ["reflection"]
        widgets = {
            "reflection": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 3,
                "placeholder": "Optional: What did you notice?"
            }),
        }