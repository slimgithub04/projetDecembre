from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Commentaire
from penality.models import Penalite
from .ai_service import CommentaireAIService  # Classe AI
from django.utils.translation import gettext as _

# Initialiser le service d'analyse des commentaires
commentaire_service = CommentaireAIService()

@receiver(post_save, sender=Commentaire)
def analyser_commentaire_et_gestion(sender, instance, created, **kwargs):
    """
    Analyse le commentaire nouvellement créé et applique les règles.
    """
    if created:  # Si un nouveau commentaire est créé
        texte_commentaire = instance.texte

        # Étape 1 : Analyse du commentaire
        analyse_resultat = commentaire_service.analyser_sentiment(texte_commentaire)
        sentiment = analyse_resultat['sentiment']
        langue_detectee = analyse_resultat['langue_detectee']

        # Mise à jour du champ langue avec le résultat de la détection de langue
        instance.langue = langue_detectee
        instance.save(update_fields=['langue'])  # Sauvegarder le champ langue

        # Étape 2 : Vérification de la toxicité
        est_approprie = commentaire_service.filtrer_commentaires_inappropries(texte_commentaire)

        if not est_approprie or sentiment == 'NEGATIVE':
            # Étape 3 : Supprimer le commentaire et créer une pénalité
            instance.delete()  # Supprime le commentaire

            # Créer une pénalité de type "harcèlement"
            Penalite.objects.create(
                utilisateur=instance.utilisateur,
                type_penalite='harcelement',
                description=_(
                    f"Un commentaire inapproprié ou toxique a été détecté : '{texte_commentaire[:50]}...'"
                ),
                gravite=3,  # Gravité élevée pour commentaires toxiques
                occurrences=1,
                supprimer_compte=False  # Décision de suppression manuelle
            )
        else:
            # Étape 4 : Mettre à jour les champs du commentaire
            instance.sentiment = sentiment
            instance.save(update_fields=['sentiment'])
