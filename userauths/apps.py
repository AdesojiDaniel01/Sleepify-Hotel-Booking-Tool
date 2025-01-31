from django.apps import AppConfig


# Configuration class for the 'userauths' app
# This class defines the configuration for the 'userauths' application and is used by Django to set up the app
class UserauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauths'
