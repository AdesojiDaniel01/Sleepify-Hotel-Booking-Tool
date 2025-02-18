from django.urls import path
from hotel import views


# Defines the app name to organize the URL namespace
app_name = "hotel"


# URL patterns that map different views to specific URLs
urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug>/", views.hotel_detail, name="hotel_detail"),
    path("detail/<slug>/room-type/<slug:rt_slug>/",
         views.room_type_detail, name="room_type_detail"),
    path("selected_rooms/", views.selected_rooms, name="selected_rooms"),
    path("checkout/<booking_id>", views.checkout, name="checkout"),
    path("update_room_status/", views.update_room_status,
         name="update_room_status"),

    # Payment API
    path('api/checkout-session/<booking_id>/',
         views.create_checkout_session, name='api_checkout_session'),
    path('success/<booking_id>/', views.payment_success, name='success'),
    path('failed/<booking_id>/', views.payment_failed, name='failed'),

]
