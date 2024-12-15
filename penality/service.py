"""
from datetime import datetime  # Import datetime instead of timezone
from transformers import pipeline
import openai
from textblob import TextBlob
import re

class PenaliteAnalyzer:
    def __init__(self):
        try:
            self.sentiment_classifier = pipeline("text-classification", model="distilbert-base-uncased")
            self.toxic_classifier = pipeline("text-classification", model="unitary/toxic-bert")
        except Exception as e:
            print(f"Erreur de chargement des modèles : {e}")
            self.sentiment_classifier = None
            self.toxic_classifier = None

    def analyze_reclamation(self, reclamation_text, user, existing_penalites):
        
        # Analyse des scores
        sentiment_score = self._analyze_sentiment(reclamation_text)
        toxicity_score = self._analyze_toxicity(reclamation_text)
        keyword_score = self._analyze_keywords(reclamation_text)
        user_history_score = self._analyze_user_history(existing_penalites)

        final_score = (
            sentiment_score * 0.2 +
            toxicity_score * 0.3 +
            keyword_score * 0.3 +
            user_history_score * 0.2
        )

        penalite_type = self._map_to_penalite_type(final_score, reclamation_text)
        gravite = self._map_to_gravite(final_score)
        supprimer_compte = final_score > 0.9
        occurrences = len(existing_penalites) + 1

        return {
            'utilisateur': user,
            'type_penalite': penalite_type,
            'description': self._generate_description(penalite_type, gravite, reclamation_text),
            'gravite': gravite,
            'occurrences': occurrences,
            'supprimer_compte': supprimer_compte,
            'score_analyse': final_score
        }

    def _analyze_sentiment(self, text):
        if not self.sentiment_classifier:
            return 0.5
        try:
            blob = TextBlob(text)
            return (blob.sentiment.polarity + 1) / 2
        except Exception:
            return 0.5

    def _analyze_toxicity(self, text):
        if not self.toxic_classifier:
            return 0.5
        try:
            result = self.toxic_classifier(text)[0]
            return result['score']
        except Exception:
            return 0.5

    def _analyze_keywords(self, text):
        keywords = {'annulation': ['annulation', 'last minute', 'retard'], 'harcelement': ['insulte', 'menace']}
        score = sum(1 for k in keywords if any(word in text.lower() for word in keywords[k]))
        return min(score, 1.0)

    def _analyze_user_history(self, existing_penalites):
        recent_penalites = [p for p in existing_penalites if (datetime.now() - p.date_penalite).days < 180]
        return min(sum(p.gravite * 0.2 for p in recent_penalites), 1.0)

    def _map_to_penalite_type(self, score, text):
        if score > 0.8:
            return 'harcelement'
        elif 'annulation' in text.lower():
            return 'annulation_tardive'
        return 'point_descente_faux'

    def _map_to_gravite(self, score):
        if score > 0.8:
            return 3
        elif score > 0.5:
            return 2
        return 1

    def _generate_description(self, type_penalite, gravite, text):
        gravite_labels = {1: 'Mineure', 2: 'Moyenne', 3: 'Grave'}
        return f"Type : {type_penalite}, Gravité : {gravite_labels[gravite]}, Extrait : {text[:150]}"
"""

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
