from django.urls import path
from userauths import views


# Defines the app name to organize the URL namespace
app_name = "userauths"


# Define the URL patterns for the userauths app
urlpatterns = [
    path("sign-up/", views.RegisterView, name="sign-up"),
    path("sign-in/", views.loginViewTemp, name="sign-in"),
    path("sign-out/", views.LogoutView, name="sign-out"),

]
