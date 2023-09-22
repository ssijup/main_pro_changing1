from django.apps import AppConfig


class NetmagicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'netmagics'

    def ready(self):
        import netmagics.signals