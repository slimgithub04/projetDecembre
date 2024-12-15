from django import forms
from .models import Commentaire
from django.core.exceptions import ValidationError

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte', 'gif']
        widgets = {
            'texte': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'class': 'form-control emoji-enabled',
                'placeholder': 'Écrivez votre commentaire ici... 😊',
                'id': 'id_texte'
            }),
            'gif': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': '.gif'
            })
        }

    def clean_texte(self):
        texte = self.cleaned_data.get('texte')
        if texte and len(texte) > 500:
            raise ValidationError("Le commentaire ne peut pas dépasser 500 caractères.")
        return texte

    