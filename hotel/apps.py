from django.apps import AppConfig


# Configuration class for the 'hotel' app
# This class defines the configuration for the 'hotel' application and is used by Django to set up the app
class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'
