from django.db import models
from django.core.exceptions import ValidationError
from evaluation.models import Evaluation
from users.models import Users
from Trip.models import Trajet

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(Users, on_delete=models.CASCADE, default=1) 
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, null=True, blank=True)
    texte = models.TextField(blank=True, null=True)  
    date_commentaire = models.DateTimeField(auto_now_add=True)  
    sentiment = models.CharField(max_length=20, blank=True, null=True, default="NEUTRAL")
    
    # Nouveau champ pour la langue ou le dialecte
    langue = models.CharField(max_length=10, blank=True, null=True)  # Champ pour stocker la langue/dialecte

    # Nouveau champ pour le GIF
    gif = models.ImageField(upload_to='commentaires/gifs/', null=True, blank=True)

    def __str__(self):
        return f"Commentaire de {self.utilisateur}  sur trajet {self.trajet or 'N/A'}"

    class Meta:
        ordering = ['date_commentaire']
