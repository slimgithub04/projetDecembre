from django import forms
from .models import Reclamation
"""
class ReclamationForm(forms.ModelForm):
    # Champ pour sélectionner un groupe (optionnel)
    groupe = forms.ModelChoiceField(
        queryset=None,  # Sera défini dans __init__
        required=False,
        label='Groupe associé (optionnel)'
    )
    
    # Champs pour les témoins
    temoin_nom = forms.CharField(
        max_length=200, 
        required=False, 
        label='Nom du témoin'
    )
    temoin_contact = forms.CharField(
        max_length=200, 
        required=False, 
        label='Contact du témoin'
    )
    temoin_role = forms.CharField(
        max_length=200, 
        required=False, 
        label='Rôle du témoin'
    )

    class Meta:
        model = Reclamation
        fields = [
            'statut_participation',
            'nom_prenom', 
            'statut_personnel', 
            'numero_telephone', 
            'date_incident', 
            'heure_incident', 
            'lieu_incident', 
            'description_incident', 
            'preuve'
        ]
        widgets = {
            'date_incident': forms.DateInput(attrs={'type': 'date'}),
            'heure_incident': forms.TimeInput(attrs={'type': 'time'}),
            'description_incident': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limiter les groupes aux groupes de l'utilisateur
        if user:
            self.fields['groupe'].queryset = user.carpool_groups.all()

    def clean(self):
        cleaned_data = super().clean()
        
        # Logique de validation des témoins
        temoin_nom = cleaned_data.get('temoin_nom')
        temoin_contact = cleaned_data.get('temoin_contact')
        temoin_role = cleaned_data.get('temoin_role')
        
        # Si un nom de témoin est fourni, créer une entrée pour les témoins
        if temoin_nom:
            temoins = [{
                'nom': temoin_nom,
                'contact': temoin_contact,
                'role': temoin_role
            }]
            cleaned_data['temoins'] = temoins
        
        return cleaned_data

"""
from django import forms
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from .models import Reclamation

class ReclamationForm(forms.ModelForm):
    # Champ pour sélectionner un groupe (optionnel)
    groupe = forms.ModelChoiceField(
        queryset=None,  # Sera défini dans __init__
        required=False,
        label='Groupe associé (optionnel)'
    )
    
    # Champs pour les témoins
    temoin_nom = forms.CharField(
        max_length=200, 
        required=False, 
        label='Nom du témoin'
    )
    temoin_contact = forms.CharField(
        max_length=200, 
        required=False, 
        label='Contact du témoin'
    )
    temoin_role = forms.CharField(
        max_length=200, 
        required=False, 
        label='Rôle du témoin'
    )

    # Validation spécifique pour la description avec support speech-to-text
    description_incident = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6, 
            'cols': 50, 
            'placeholder': 'Décrivez l\'incident en détail... Vous pouvez utiliser la dictée vocale.',
            'class': 'form-control'
        }),
        validators=[
            MaxLengthValidator(2000, message='La description ne doit pas dépasser 2000 caractères.'),
        ],
        required=True,
        help_text='Utilisez le bouton de microphone pour la dictée vocale si nécessaire.'
    )

    # Validation personnalisée pour les fichiers
    preuve = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'],
                message='Formats acceptés : PDF, JPG, PNG, DOC'
            )
        ],
        help_text='Formats acceptés : PDF, JPG, PNG, DOC (max 5 Mo)',
        required=False
    )

    class Meta:
        model = Reclamation
        fields = [
            'statut_participation',
            'nom_prenom', 
            'statut_personnel', 
            'numero_telephone', 
            'date_incident', 
            'heure_incident', 
            'lieu_incident', 
            'description_incident', 
            'preuve'
        ]
        widgets = {
            'date_incident': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_incident': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'nom_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_telephone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'statut_personnel': forms.Select(attrs={'class': 'form-control'}),
            'lieu_incident': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Personnalisation des messages d'erreur
        self.fields['nom_prenom'].error_messages['required'] = 'Veuillez saisir votre nom et prénom.'
        self.fields['numero_telephone'].error_messages['required'] = 'Veuillez saisir votre numéro de téléphone.'
        
        # Limitation des groupes aux groupes de l'utilisateur
        if user:
            self.fields['groupe'].queryset = user.carpool_groups.all()

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation des témoins
        temoin_nom = cleaned_data.get('temoin_nom')
        temoin_contact = cleaned_data.get('temoin_contact')
        temoin_role = cleaned_data.get('temoin_role')
        
        # Logique de validation des témoins
        if temoin_nom:
            if not temoin_contact:
                self.add_error('temoin_contact', 'Un contact est requis pour le témoin.')
            
            temoins = [{
                'nom': temoin_nom,
                'contact': temoin_contact,
                'role': temoin_role or 'Non spécifié'
            }]
            cleaned_data['temoins'] = temoins
        
        # Validation de la taille du fichier
        preuve = cleaned_data.get('preuve')
        if preuve:
            if preuve.size > 5 * 1024 * 1024:  # 5 Mo
                self.add_error('preuve', 'Le fichier ne doit pas dépasser 5 Mo.')
        
        return cleaned_data

    def clean_description_incident(self):
        description = self.cleaned_data.get('description_incident', '')
        
        # Nettoyage et validation supplémentaire du texte
        description = description.strip()
        
        if len(description) < 20:
            raise forms.ValidationError('La description doit contenir au moins 20 caractères.')
        
        return description

"""
from django import forms
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from .models import Reclamation

class ReclamationForm(forms.ModelForm):
    # Champ pour sélectionner un groupe (optionnel)
    groupe = forms.ModelChoiceField(
        queryset=None,  # Sera défini dans __init__
        required=False,
        label='Groupe associé (optionnel)'
    )
    
    # Champs pour les témoins
    temoin_nom = forms.CharField(
        max_length=200, 
        required=False, 
        label='Nom du témoin'
    )
    temoin_contact = forms.CharField(
        max_length=200, 
        required=False, 
        label='Contact du témoin'
    )
    temoin_role = forms.CharField(
        max_length=200, 
        required=False, 
        label='Rôle du témoin'
    )

    class Meta:
        model = Reclamation
        fields = [
            'statut_participation',
            'nom_prenom', 
            'statut_personnel', 
            'numero_telephone', 
            'date_incident', 
            'heure_incident', 
            'lieu_incident', 
            'description_incident', 
            'preuve'
        ]
        widgets = {
            'date_incident': forms.DateInput(attrs={'type': 'date'}),
            'heure_incident': forms.TimeInput(attrs={'type': 'time'}),
            'description_incident': forms.Textarea(attrs={
                'rows': 6, 
                'cols': 50, 
                'placeholder': 'Décrivez l\'incident en détail... Vous pouvez utiliser la dictée vocale.',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limiter les groupes aux groupes de l'utilisateur
        if user:
            self.fields['groupe'].queryset = user.carpool_groups.all()

    def clean(self):
        cleaned_data = super().clean()
        
        # Logique de validation des témoins
        temoin_nom = cleaned_data.get('temoin_nom')
        temoin_contact = cleaned_data.get('temoin_contact')
        temoin_role = cleaned_data.get('temoin_role')
        
        # Si un nom de témoin est fourni, créer une entrée pour les témoins
        if temoin_nom:
            temoins = [{
                'nom': temoin_nom,
                'contact': temoin_contact,
                'role': temoin_role
            }]
            cleaned_data['temoins'] = temoins
        
        # Validation de la description
        description = cleaned_data.get('description_incident', '')
        if len(description.strip()) < 20:
            self.add_error('description_incident', 'La description doit contenir au moins 20 caractères.')
        
        # Validation de la taille du fichier
        preuve = cleaned_data.get('preuve')
        if preuve:
            if preuve.size > 5 * 1024 * 1024:  # 5 Mo
                self.add_error('preuve', 'Le fichier ne doit pas dépasser 5 Mo.')
        
        return cleaned_data
    
"""
    
