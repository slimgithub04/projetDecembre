from django.db import models
from users.models import Users
from django.core.validators import FileExtensionValidator
from group.models import Carpool
from django.utils.timezone import now


class Reclamation(models.Model):
    STATUTS_CHOICES = [
        ('en_cours', 'En cours'),
        ('resolue', 'Résolue'),
        ('en_attente', 'En attente')
    ]

    STATUT_PARTICIPATION_CHOICES = [
        ('individuel', 'Participation Individuelle'),
        ('groupe', 'Participation de Groupe')
    ]

    STATUT_PERSONNEL_CHOICES = [
        ('conducteur', 'Conducteur'),
        ('passager', 'Passager'),
        ('autre', 'Autre')
    ]

    # Utilisateur qui dépose la réclamation
    utilisateur = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reclamations')
    
    # Type de participation
    statut_participation = models.CharField(
        max_length=50, 
        choices=STATUT_PARTICIPATION_CHOICES, 
        default='individuel'
    )
    
    # Groupe associé (optionnel)
    groupe = models.ForeignKey(
        Carpool, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reclamations'
    )
    
    # Informations personnelles
    nom_prenom = models.CharField(max_length=200,default="user user")
    statut_personnel = models.CharField(max_length=50, choices=STATUT_PERSONNEL_CHOICES, default="Participation Individuelle")
    numero_telephone = models.CharField(max_length=20,default="00 000 000")
    
    # Détails de l'incident
    date_incident = models.DateField(default=now)
    heure_incident = models.TimeField(default="08:00")
    lieu_incident = models.CharField(max_length=200,default="Lieu de l'incident ")
    
    # Description de l'incident
    description_incident = models.TextField()
    
    # Témoins (avec une structure plus flexible)
    temoins = models.JSONField(null=True, blank=True, help_text="Informations sur les témoins")
    
    # Preuve documentaire
    preuve = models.FileField(
        upload_to='reclamations/preuves/', 
        null=True, 
        blank=True, 
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
            )
        ]
    )
    
    # Métadonnées de la réclamation
    date_reclamation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=STATUTS_CHOICES, default='en_cours')
    
    def __str__(self):
        return f"Réclamation {self.id} - {self.nom_prenom}"
    
    def ajouter_temoin(self, nom, contact=None, role=None):
        """
        Méthode pour ajouter un témoin de manière structurée
        """
        if not self.temoins:
            self.temoins = []
        
        temoin = {
            'nom': nom,
            'contact': contact,
            'role': role
        }
        
        self.temoins.append(temoin)
        self.save()
    
    def get_temoins(self):
        """
        Récupère la liste des témoins
        """
        return self.temoins or []
    

from django.db import models
from django.utils.timezone import now


class AnalyseReclamationAvecAI(models.Model):
    # La réclamation à laquelle l'analyse est liée
    reclamation = models.OneToOneField(Reclamation, on_delete=models.CASCADE, related_name='analyse')

    # Type de pénalité généré par l'IA
    type_penalite = models.CharField(max_length=100, blank=True, null=True)

    # Score de l'IA
    score_analyse = models.FloatField(default=0.0)

    # Statut de validation par un administrateur (True si validée, False sinon)
    validee = models.BooleanField(default=False)

    # Date de l'analyse
    date_analyse = models.DateTimeField(default=now)

    # Utilisateur cible (par défaut 'admin')
    utilisateurcible = models.ForeignKey(Users, on_delete=models.SET_DEFAULT, default=1)  # Assuming '1' is the ID of the 'admin' user


    def __str__(self):
        return f"Analyse pour réclamation {self.reclamation.id} - Validée : {self.validee} - Utilisateur Cible : {self.utilisateurcible}"
