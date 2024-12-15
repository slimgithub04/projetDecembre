from django.db import models
from users.models import Users
from django.core.exceptions import ValidationError
from django.utils import timezone
from Trip.models import Trajet

# Fonction de validation pour la date de l'évaluation
def validate_date_evaluation(value):
    if value > timezone.now():
        raise ValidationError('La date de l\'évaluation ne peut pas être dans le futur.')

class Evaluation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    evaluateur = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='evaluations_donnees')
    role_evaluateur = models.CharField(max_length=15, editable=False, default='Utilisateur')  # Rôle de l'évaluateur (ex. 'Utilisateur', 'Admin')
    
    # Nouveaux champs d'évaluation
    communication = models.PositiveSmallIntegerField(default=0)  # Communication (0-10)
    ponctualite = models.PositiveSmallIntegerField(default=0)  # Ponctualité du conducteur (0-10)
    confort = models.PositiveSmallIntegerField(default=0)  # Confort du trajet (0-10)
    
    # Calcul de la note totale (sur 100)
    note = models.PositiveSmallIntegerField(default=0)  # Note sur 100
    date_evaluation = models.DateTimeField(auto_now_add=True, validators=[validate_date_evaluation])

    def save(self, *args, **kwargs):
        """
        Avant de sauvegarder, met à jour le rôle de l'évaluateur à partir de son modèle
        et calcule la note finale sur 100 en fonction des pondérations.
        """
        if self.evaluateur:
            self.role_evaluateur = self.evaluateur.role
        
        # Calcul de la note sur 30 en fonction des critères
        total_score = self.communication + self.ponctualite + self.confort
        
        # Calcul de la note sur 100
        self.note = (total_score / 30) * 100

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Évaluation de {self.evaluateur.email} (Rôle : {self.role_evaluateur}) pour le trajet {self.trajet.id}"

    class Meta:
        indexes = [
            models.Index(fields=['trajet', 'evaluateur']),  # Ajoute un index composite pour trajet et évaluateur
        ]
