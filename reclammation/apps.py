from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reclammation'  # Remplacez `myapp` par le nom de votre application

    def ready(self):
        """
        Cette méthode est appelée lorsque l'application est prête.
        Elle importe les signaux pour s'assurer qu'ils sont connectés.
        """
        import reclammation.signals  # Remplacez `myapp` par le nom de votre application
