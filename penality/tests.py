from django.test import TestCase
from datetime import datetime, timedelta

from service import classify_penalty  # Import the PenaliteAnalyzer class

def test_model():
    complaints = [
        "Je suis très déçu car on m'a demandé de payer mais le paiement n'a pas été pris en compte.",
        "Le chauffeur a choisi un mauvais point de descente, ce qui m'a causé beaucoup de problèmes.",
        "Il n'y avait pas assez de places disponibles comme indiqué lors de la réservation.",
        "On m'a harcelé pour quitter le véhicule sans raison valable.",
        "Les bagages que j'avais réservés n'étaient pas pris en charge correctement.",
        "J'ai essayé d'annuler mais cela a été fait trop tard et j'ai été pénalisé.",
        "Je n'ai pas pu trouver de place dans le bus malgré ma réservation confirmée.",
        "Le chauffeur a été extrêmement impoli et m'a intimidé pendant tout le trajet.",
        "On m'a facturé deux fois pour un seul billet, ce qui est inacceptable.",
        "Le véhicule n'avait pas l'espace prévu pour les bagages, comme précisé lors de la réservation.",
        "La demande d'annulation que j'ai soumise n'a pas été acceptée et j'ai perdu tout mon argent.",
        "Le point de descente prévu était incorrect et je me suis retrouvé loin de ma destination finale.",
        "Malgré mon paiement à l'avance, mon billet n'a pas été validé par le système.",
        "On m'a réprimandé publiquement devant les autres passagers sans raison justifiée.",
        "Les informations sur les places disponibles étaient erronées et j'ai dû attendre un autre bus.",
        "J'ai été maltraité verbalement par le personnel de l'agence.",
        "Mon paiement a été refusé malgré un solde suffisant sur ma carte bancaire.",
        "Le point d'arrêt était à un endroit dangereux et non conforme aux normes.",
        "Il y avait des frais supplémentaires pour les bagages sans explication claire.",
        "Le système a confirmé une annulation mais je n'ai pas reçu de remboursement."
    ]

    for complaint in complaints:
        result = classify_penalty(complaint)
        print(f"Reclamation: {complaint}")
        print(f"Code de la pénalité: {result['penalty_code']}")
        print(f"Libellé de la pénalité: {result['penalty_label']}")
        print(f"Confiance: {result['confidence']:.2f}\n")

if __name__ == "__main__":
    test_model()