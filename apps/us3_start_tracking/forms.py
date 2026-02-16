from django import forms
from datetime import date


class StartTrackingForm(forms.Form):
    avg_cycle_length = forms.IntegerField(
        label="Average cycle length (days)",
        min_value=1,
        max_value=30,
        error_messages={
            "min_value": "Cycle length must be at least 1 days.",
            "max_value": "Cycle length must be 30 days or fewer.",
            "invalid": "Please enter a whole number.",
        },
    )

    last_period_start = forms.DateField(
        label="Last period start date",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    def clean_last_period_start(self):
        d = self.cleaned_data["last_period_start"]
        if d > date.today():
            raise forms.ValidationError(
                "Last period start date cannot be in the future."
            )
        return d

