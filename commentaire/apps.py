from django.apps import AppConfig

class CommentaireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commentaire'

    def ready(self):
        import commentaire.signals  # Enregistrer les signaux
