from django.apps import AppConfig


class AplicacionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aplicacion"

from django.apps import AppConfig

class AeropuertoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_aeropuerto'

    def ready(self):
        import app_aeropuerto.signals  # Importa las señales al iniciar la app
