from django.apps import AppConfig

class AppMainConfig(AppConfig):  # ← nom unique
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'