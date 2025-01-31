from django.apps import AppConfig


# Configuration class for the 'booking' app
# This class defines the configuration for the 'booking' application and is used by Django to set up the app
class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'
