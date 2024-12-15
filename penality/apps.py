from django.apps import AppConfig


class PenalityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'penality'
    def ready(self):
        import penality.signals  # Assurez-vous que le signal est chargé



    

