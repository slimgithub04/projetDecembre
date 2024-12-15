from django import forms
from django.utils import timezone

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date', 
                'class': 'form-control',  # Ajout d'une classe pour un style cohérent
                'placeholder': 'Sélectionnez une date de début'
            }
        ),
        initial=timezone.now().date() - timezone.timedelta(days=30),
        label="Date de début"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date', 
                'class': 'form-control',  # Ajout d'une classe pour un style cohérent
                'placeholder': 'Sélectionnez une date de fin'
            }
        ),
        initial=timezone.now().date(),
        label="Date de fin"
    )
