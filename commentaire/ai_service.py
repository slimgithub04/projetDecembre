from transformers import pipeline
from langdetect import detect
import re

class CommentaireAIService:
    def __init__(self):
        # Pipeline d'analyse de sentiment (avec prise en charge des sentiments neutres)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", 
            model="cardiffnlp/twitter-roberta-base-sentiment"
        )

        # Pipeline de traduction vers l'anglais
        self.translator_to_english = pipeline(
            "translation", 
            model="Helsinki-NLP/opus-mt-mul-en"  # Modèle multilingue -> anglais
        )
        
        # Modèle pour la détection des dialectes arabes
        self.dialect_identifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            tokenizer="facebook/bart-large-mnli"
        )

        # Pipeline pour la détection de contenu inapproprié
        self.toxicity_detector = pipeline(
            "text-classification", 
            model="unitary/toxic-bert",  # Vous pouvez aussi utiliser HateXplain si disponible
            return_all_scores=True
        )
    
    def detecter_langue(self, commentaire):
        """
        Détecte la langue du commentaire en détectant les dialectes arabes et autres langues.
        """
        try:
            # Utiliser langdetect pour les langues courantes
            langue = detect(commentaire)
            
            # Si la langue détectée est l'arabe, on passe à une détection de dialecte plus précise
            if langue == 'ar':
                dialectes_possibles = ['ar-tun', 'ar-eg', 'ar-sa', 'ar-dz', 'ar-ma', 'ar-ly']
                # Utilisation d'un modèle pour identifier un dialecte spécifique
                result = self.dialect_identifier(commentaire, candidate_labels=dialectes_possibles)
                langue = result['labels'][0]  # Prendre le dialecte le plus probable
            
            return langue
        
        except Exception as e:
            print(f"Erreur de détection de langue: {e}")
            return 'error'

    def traduire_vers_anglais(self, commentaire):
        """
        Traduit le commentaire vers l'anglais si nécessaire.
        """
        try:
            result = self.translator_to_english(commentaire)
            return result[0]['translation_text']
        except Exception as e:
            print(f"Erreur de traduction: {e}")
            return commentaire  # Retourner le commentaire original en cas d'erreur de traduction
    
    def analyser_sentiment(self, commentaire):
        """
        Analyse le sentiment du commentaire en gérant plusieurs langues, avec prise en charge explicite des sentiments neutres.
        """
        try:
            # Étape 1: Détection de la langue
            langue = self.detecter_langue(commentaire)

            # Étape 2: Traduction si nécessaire
            if langue != 'en':  # Si la langue n'est pas l'anglais
                commentaire = self.traduire_vers_anglais(commentaire)

            # Étape 3: Analyse de sentiment
            result = self.sentiment_analyzer(commentaire)[0]

            # Mappage des labels en sentiments textuels
            sentiment_map = {
                'LABEL_0': 'NEGATIVE',
                'LABEL_1': 'NEUTRAL',
                'LABEL_2': 'POSITIVE'
            }

            # Récupération du sentiment et du score
            sentiment = sentiment_map.get(result['label'], 'NEUTRAL')  # Par défaut 'NEUTRAL' si le label n'est pas reconnu
            score = result['score']

            return {
                'langue_detectee': langue,
                'sentiment': sentiment,
                'score': score  # Confiance du modèle (0 à 1)
            }
        except Exception as e:
            print(f"Erreur d'analyse de sentiment: {e}")
            return {
                'langue_detectee': 'error',
                'sentiment': 'NEUTRAL',
                'score': 0.5  # Valeur par défaut pour l'erreur
            }

    def filtrer_commentaires_inappropries(self, commentaire):
        """
        Utiliser un modèle dédié pour détecter des commentaires inappropriés, y compris insultes, haine et vulgarités.
        """
        try:
            # Obtenir les scores de probabilité pour chaque classe
            results = self.toxicity_detector(commentaire)

            # Recherche des scores liés à la toxicité
            toxic_score = 0
            for result in results[0]:  # Accéder à toutes les classes
                if result['label'].lower() == 'toxic':
                    toxic_score = result['score']
                    break

            # Seuil pour juger un commentaire inapproprié
            seuil = 0.5  # Ajustable selon le besoin

            return toxic_score < seuil  # Approprié si toxicité inférieure au seuil
        except Exception as e:
            print(f"Erreur de détection de contenu inapproprié: {e}")
            return True  # Considérer le commentaire comme approprié en cas d'erreur
