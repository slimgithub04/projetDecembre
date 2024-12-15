from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Reclamation
from .models import Reclamation, AnalyseReclamationAvecAI
from transformers import pipeline
from googletrans import Translator  # Install with `pip install googletrans==4.0.0-rc1`

def classify_penalty(text):
    """
    Classify a user complaint into predefined penalty categories for multiple languages.
    
    Args:
        text (str): User complaint text in any language.
    
    Returns:
        dict: A dictionary with the penalty code, label, and confidence score.
    """
    # Translate the text to English
    translator = Translator()
    translated_text = translator.translate(text, src='auto', dest='en').text

    # Load the zero-shot classification model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    # Define penalty categories
    TYPE_PENALITE_CHOICES = [
        ('annulation_tardive', 'Annulation tardive ou de dernière minute'),
        ('annulation_sans_informer', 'Annulation brusque sans informer le passager'),
        ('harcelement', 'Harcèlement ou comportement inapproprié'),
        ('point_descente_faux', 'Point de descente incorrect ou imprécis '),
        ('nombre_places_incorrect', 'Nombre de places incorrect ou non-respecté'),
        ('disponibilite_bagages_incorrecte', 'Disponibilité des bagages non conforme'),
        ('paiement_non_effectue', 'Paiement non effectué '),
        ('retard_significatif', 'Retard significatif au point de rendez-vous'),
        ('non_presentation', 'Non-présentation au rendez-vous sans annulation'),
        ('autres', 'Autres problèmes non spécifiés technical problemes techniques de systeme et paiement refusé ou pas pris en compte'),
    ]


    labels = [label[1] for label in TYPE_PENALITE_CHOICES]

    # Perform classification
    result = classifier(translated_text, labels)
    classified_label = result['labels'][0]
    classified_score = result['scores'][0]

    # Map classified label to penalty code
    for code, label in TYPE_PENALITE_CHOICES:
        if label == classified_label:
            return {
                'penalty_code': code,
                'penalty_label': classified_label,
                'confidence': classified_score
            }

    # Default fallback
    return {
        'penalty_code': 'others',
        'penalty_label': 'Other issues',
        'confidence': classified_score
    }


@receiver(post_save, sender=Reclamation)
def envoyer_mail_reclamation(sender, instance, created, **kwargs):
    """
    Signal pour envoyer un e-mail lorsqu'une réclamation est créée.
    """
    if created:
        sujet = "Confirmation de votre réclamation"
        message = f"""
        Bonjour {instance.nom_prenom},

        Votre réclamation a bien été enregistrée et sera traitée prochainement par notre équipe administrative et notre système d'intelligence artificielle.

        **Détails de la réclamation :**
        - **Numéro de réclamation :** {instance.id}
        - **Date de l'incident :** {instance.date_incident}
        - **Heure de l'incident :** {instance.heure_incident}
        - **Lieu de l'incident :** {instance.lieu_incident}
        - **Description :** {instance.description_incident}

        Nous vous remercions pour votre confiance. Notre équipe est à votre disposition si vous avez des questions ou des précisions à apporter.

        Cordialement,  
        L'équipe de gestion des réclamations
        wasalni
        """
        send_mail(
            subject=sujet,
            message=message,
            from_email="noreply@votreentreprise.com",  # Remplacez par l'adresse de votre système
            recipient_list=[instance.utilisateur.email],  # Utilisez l'email de l'utilisateur
            fail_silently=False,
        )



# Signal qui sera déclenché après l'enregistrement d'une nouvelle réclamation
@receiver(post_save, sender=Reclamation)
def analyse_reclamation_after_save(sender, instance, created, **kwargs):
    """
    Ce signal analyse la réclamation et remplit le modèle `AnalyseReclamationAI`.
    """
    if created:
        # Utilisation de l'IA pour analyser la réclamation
        result = classify_penalty(instance.description_incident)

        # Créer une nouvelle analyse de réclamation liée
        AnalyseReclamationAvecAI.objects.create(
            reclamation=instance,
            type_penalite=result['penalty_code'],
            score_analyse=result['confidence'],
        )



