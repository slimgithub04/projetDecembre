from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Penalite

@receiver(post_save, sender=Penalite)
def envoyer_email_penalite_grave(sender, instance, created, **kwargs):
    """
    Envoie un email automatique en cas de pénalité grave ou de suppression de compte.
    """
    if created and (instance.gravite == 3 or instance.supprimer_compte):
        utilisateur = instance.utilisateur
        sujet = "Alerte : Pénalité grave sur votre compte"
        message = (
            f"Bonjour {utilisateur.email},\n\n"
            "Une pénalité grave a été ajoutée à votre compte.\n\n"
            f"**Détails :**\n"
            f"Type : {instance.get_type_penalite_display()}\n"
            f"Gravité : {instance.get_gravite_display()}\n"
            f"Description : {instance.description}\n\n"
            "Cette pénalité pourrait entraîner la suppression de votre compte.\n"
            "Si vous avez des questions ou si vous souhaitez contester cette décision, veuillez nous contacter immédiatement.\n\n"
            "Cordialement,\nL'équipe de gestion"
        )
        try:
            send_mail(
                sujet,
                message,
                'your-email@gmail.com',  # Remplacez par l'adresse expéditrice
                [utilisateur.email],     # Destinataire
                fail_silently=False,
            )
        except Exception as e:
            # Vous pouvez enregistrer l'erreur dans les logs si vous le souhaitez
            print(f"Erreur lors de l'envoi de l'email : {str(e)}")


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Penalite
from reclammation.models import AnalyseReclamationAvecAI
from django.utils import timezone

@receiver(post_save, sender=AnalyseReclamationAvecAI)
def create_penalite_from_AnalyseReclamationAI(sender, instance, created, **kwargs):
    if instance.validee:  # Si la réclamation a été validée
        # Vérifiez si la pénalité existe déjà pour l'utilisateur avec le même type de pénalité.
        penalite, created = Penalite.objects.get_or_create(
            utilisateur=instance.utilisateurcible,  # Récupérer l'utilisateur de la réclamation
            type_penalite=instance.type_penalite,  # Le type de pénalité à partir de l'analyse
            defaults={
                'description': f"Pénalité générée suite à la réclamation validée : {instance.type_penalite}",
                'gravite': 2,  # Exemple de gravité. Vous pouvez ajuster cela selon votre logique
                'occurrences': 1,
                'score_analyse': instance.score_analyse,
                'date_penalite': timezone.now(),
                'supprimer_compte': False,
            }
        )

        if not created:
            # Si la pénalité existe déjà, on peut mettre à jour certaines valeurs, si nécessaire
            penalite.score_analyse = instance.score_analyse
            penalite.save()

        # Facultatif: Vous pouvez ajouter des logs ou des actions supplémentaires ici
        print(f"Pénalité {penalite.type_penalite} pour {penalite.utilisateur} a été créée ou mise à jour.")



        


