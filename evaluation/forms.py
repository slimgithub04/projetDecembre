from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['communication', 'ponctualite', 'confort']  # Ajouter 'note' dans les champs mais caché

        widgets = {
            'communication': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0',
                'max': '10',
                'step': '0.1',
                'class': 'form-range',
                'id': 'communication-slider'
            }),
            'ponctualite': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0',
                'max': '10',
                'step': '0.1',
                'class': 'form-range',
                'id': 'ponctualite-slider'
            }),
            'confort': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0',
                'max': '10',
                'step': '0.1',
                'class': 'form-range',
                'id': 'confort-slider'
            }),
            
        }

        labels = {
            'communication': 'Communication',
            'ponctualite': 'Ponctualité du conducteur',
            'confort': 'Confort du trajet',
            
        }
